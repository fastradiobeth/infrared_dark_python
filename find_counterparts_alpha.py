
# find_counterparts_alpha.py
# ******************************************************************************
# July 2015
# Beth Jones
# School of Physics and Astronomy | The University of Manchester
# ******************************************************************************
# standalone code used for producing catalogues of objects found in multiple
# wavelengths using catalogues of objects found in single wavelengths
#
# 1	-	Source association by centroids
#			A reference wavelength is chosen, and a minimum separation for
#			two sources to be separate. Each reference source is compared to a
#			another single wavelength catalogue of centroids, and a counterpart
#			is assigned if there is a source within the minimum separation
#			boundary. Distances between centroids are calculated using Vincenty
#			Great Cirles. If more than one counterpart is found, the one closest
#			to the reference wavelength is saved. Sources with a counterpart in
#			all required wavelengths are saved.
#
# 2 -	Removal of separate sources resolved at shorter wavelengths only
#			As a single source in a long wavelength map can be assigned to
#			multiple reference wavelength sources due to blending at long
#			wavelengths, the subset of candidates from the first association are
#			run through a second association using the longest wavelength as the
#			reference. The two sets are then compared and only sources with the
#			same reference and longest wavelength coordinates in both sets are
#			saved. This ensures that only one reference source is associated
#			to a given longer wavelength centroid.
#
# 3 -	Removal of duplicate sources in the reference wavelength
#			As the same source may appear in multiple IRDCs due to overlap,
#			exact copies of sources remain in the subset. If more than one
#			source with a distance of zero to any given source is found in this
#			set, the entry is removed. This distance at which sources in the
#			same wavelength are considered the same source can be set to > 0
#			if required (e.g. one beamwidth)
#
# the resulting catalogue is printed to the output directory, with the source
# centroid in each wavelength
# although labelled otherwise, glat and glong are used.
print 'find_counterparts_alpha.py starting up...'
# header material
# ------------------------------------------------------------------------------
import os
import sys
import re
import math
import numpy as np
from more_itertools import unique_everseen
from astropy.coordinates import SkyCoord
from astropy import units as u

# required parameters
# ------------------------------------------------------------------------------
wavelengths = [70,160,250,350]
wavelengths_required = [70,160,250,350]
wavelengths_excluded = []
reference_wavelength = 160

cat_loc = '/home/bjones/Documents/IRDC_catalogues/'
output_loc = '/home/bjones/Desktop/'
# catalogue names based on prefix + variable wavelength - can enter strings into
# single_wl_cats manually instead with wavelengths as keys
single_wl_cats = {}
cat_prfx = 'hyper_photometry_sig_var_FWHM_10_new_run_sources_only_'
for x in wavelengths:
	single_wl_cats[x] = cat_loc + cat_prfx + str(x) + '.dat'
# relevant columns in single wavelength catalogues
map_col = [0]
coord_cols = [2,3]
headerlines = 3

# coord type
#	0	-	Galactic longitude and latitude
#	1	-	RA and DEC (J200)
coord_type = 0

# separation_type
#	0	- miniumum Hi-GAL beam of wavelengths_required (default)
#	1	- select a Hi-GAL beam_to_use as minimum separation
#	2	-  set separation for source association to value of fixed_beam
separation_type = 0
fixed_beam = 5 # arcseconds
beam_to_use = 160

# duplicate_filter_type
#	0	-	only remove exact duplicates (default)
#	1 	- 	select Hi-GAL beam separation of duplicates (filter_beam)
#	2	-	set fixed separation (fixed_filter)
#	3	- 	use same separation as for counterpart assignment
duplicate_filter_type = 3
filter_beam = 160
fixed_filter = 5 # arcseconds

# Hi-GAL beam selection
# ------------------------------------------------------------------------------
# all in arcseconds
def wavelength_to_beam(wavelength):
	higal_beams = {
		70: 10.2,
		160: 13.55,
		250: 18.0,
		350: 24.0,
		500: 34.5
	}
	return higal_beams.get(wavelength)

if separation_type == 1:
	beam = wavelength_to_beam(beam_to_use)
elif separation_type == 2:
	beam = fixed_beam
else:
	total_required = len(wavelengths_required)
	beams = np.empty(total_required)
	for x in range(total_required):
		beams[x] = wavelength_to_beam(wavelengths_required[x])
	min_beam = np.amin(beams)
	print 'minimum beam: ' + str(min_beam)
	beam = min_beam

# duplicate filter type
if duplicate_filter_type == 1:
	same_wl_beam = wavelength_to_beam(filter_beam)
elif duplicate_filter_type == 2:
	same_wl_beam = fixed_filter
elif duplicate_filter_type == 3:
	same_wl_beam = beam
else:
	same_wl_beam = 0


# check directories
# ------------------------------------------------------------------------------
if os.path.isdir(cat_loc) == False:
	sys.exit('Catalogue directory not found.')
if os.path.isdir(output_loc) == False:
	sys.exit('Output directory not found.')

# import source coordinates from catalogues
# ------------------------------------------------------------------------------

total_wavelengths = len(wavelengths)
total_required = len(wavelengths_required)

single_wl_maps ={}
dt = np.dtype('f8')
glat = {}
glon = {}
if coord_type == 1:
	ra = {}
	dec ={}

for x in wavelengths:
	single_wl_maps[x] = (np.loadtxt(single_wl_cats[x], skiprows=headerlines, usecols=map_col, dtype=np.str)).tolist()
	if coord_type == 0:
		glon[x], glat[x] = np.loadtxt(single_wl_cats[x], skiprows=headerlines, usecols=coord_cols, unpack=True, dtype=dt)
	elif coord_type == 1:
		ra[x], dec[x] = np.loadtxt(single_wl_cats[x], skiprows=headerlines, usecols=coord_cols, unpack=True, dtype=dt)
		source_coords = SkyCoord(SkyCoord(ra[x]*u.degree, dec[x]*u.degree, frame='icrs'))
		source_coords = source_coords.transform_to('galactic')
		glon[x] = source_coords.l.degree
		glat[x] = source_coords.b.degree
	else:
		sys.exit('Unknown input coordinate type, quitting...')
total_sources = len(single_wl_maps[reference_wavelength])
print 'Total reference wavelength sources:  ' + str(total_sources)

# association of sources over multiple wavelengths
# ------------------------------------------------------------------------------
# associates sources cross-wavelength by setting minimum angular distance
# to be considered a different object (default: minimum beamwidth)

def ang_sep(test_x, test_y, source_x, source_y):
	# these are fine to be arrays of (x,y) celestial coords
	# finds angular separation of test coords to source coords in degrees
	dt = np.dtype('f8')
	# convert to radians for numpy
	test_x_rad = np.radians(test_x, dtype=dt)
	test_y_rad = np.radians(test_y, dtype=dt)
	source_x_rad = np.radians(source_x, dtype=dt)
	source_y_rad = np.radians(source_y, dtype=dt)
	# Vincenty great circles angular separation
	delta_x = abs(source_x_rad - test_x_rad)
	y_term_one = (np.cos(test_y_rad)*np.sin(delta_x))**2
	y_term_two = (np.cos(source_y_rad)*np.sin(test_y_rad) - np.sin(source_y_rad)*np.cos(test_y_rad)*np.cos(delta_x))**2
	y_term = np.sqrt(y_term_one + y_term_two)
	x_term = np.sin(source_y_rad)*np.sin(test_y_rad) + np.cos(source_y_rad)*np.cos(test_y_rad)*np.cos(delta_x)
	distance = np.degrees(np.arctan2(y_term, x_term))
	return distance

# initialise variables for data output
source_glons = np.zeros((total_wavelengths, total_sources))
source_glats = np.zeros((total_wavelengths, total_sources))
source_dists = np.zeros((total_wavelengths, total_sources))
source_all_wl = np.zeros((total_wavelengths, total_sources))
print 'searching for all catalogued candidates...'

# for all wavelengths required to be considered a candidate source
for i,j in enumerate(wavelengths):
	if j == reference_wavelength:
		# this is reference wavelength
		source_all_wl[i,:] = 1
		source_glons[i,:] = glon[j]
		source_glats[i,:] = glat[j]
	else:
		for x in range(total_sources):
			other_chan = i
			total_other_wl_sources = len(single_wl_maps[j])
			# make arrays of current 160 source to compare to all other sources
			temp_glon = np.empty(total_other_wl_sources)
			temp_glat = np.empty(total_other_wl_sources)
			temp_glon.fill(glon[reference_wavelength][x])
			temp_glat.fill(glat[reference_wavelength][x])
			# make arrays of other sources
			other_source_glon = glon[j]
			other_source_glat = glat[j]
			# find distances
			dist = 3600*ang_sep(temp_glon, temp_glat, other_source_glon, other_source_glat)
			# find indicies of all sources within set distance from ref centroid
			same_source = [ind for ind, v in enumerate(dist) if v<=beam]
			num_associated_sources = len(same_source)
			if num_associated_sources != 0:
				if j in wavelengths_required:
					# is useful, save details
					source_all_wl[other_chan, x] = 1
					if num_associated_sources == 1:
						# save coordinates of counterpart
						source_glons[other_chan, x] = other_source_glon[same_source[0]]
						source_glats[other_chan, x] = other_source_glat[same_source[0]]
						source_dists[other_chan, x] = dist[same_source[0]]
					else:
						# pick closest counterpart and save coordinates
						closest_source = [ind for ind,v in enumerate(dist) if v == np.amin(dist[same_source])]
						source_glons[other_chan, x] = other_source_glon[closest_source[0]]
						source_glats[other_chan, x] = other_source_glat[closest_source[0]]
						source_dists[other_chan, x] = dist[closest_source[0]]
				elif j in wavelengths_excluded:
					# make sure source does not appear in candidates list
					source_all_wl[other_chan, x] = 800
				#else:
					# ignore, not interested in this wavelength
					# can put extra code here to do something with sources
					# detected in additional (but not required) wavelengths
			#else:
				# do not change entry in indicator array

# filter lists to contain only sources detected in all wavelengths
total_wavelengths_observed = source_all_wl.sum(axis=0)
candidate_indices = [i for i,v in enumerate(total_wavelengths_observed) if v==total_required]
candidate_indices = np.asarray(candidate_indices)
# the map assigned to each source is the map of the reference wavelength source
candidate_maps = [single_wl_maps[reference_wavelength][i] for i in candidate_indices]
candidate_glons = {}
candidate_glats = {}
candidate_dists= {}
for x in range(total_wavelengths):
	candidate_glons[wavelengths[x]] = source_glons[x,candidate_indices]
	candidate_glats[wavelengths[x]] = source_glats[x, candidate_indices]
	candidate_dists[wavelengths[x]] = source_dists[x, candidate_indices]

count_candidates = len(candidate_indices)
print 'Candidate count before duplicate source removal:  ' + str(count_candidates)

# removal of multiple sources associated to one source in a longer wavelength
# ------------------------------------------------------------------------------
# runs on candidate subset, note: all intermediate wavelengths are ignored.
print 'Removing multiple reference wavelength sources assigned to one source in longest wavelength...'
# all source coord lists are now same length
# UPDATE: no indicator array as all sources must have a counterpart to be here

higher_reference_wavelength = np.amax(wavelengths_required)
higher_wavelengths = [reference_wavelength, higher_reference_wavelength]
higher_total_wavelengths = len(higher_wavelengths)
higher_source_glons = np.zeros((higher_total_wavelengths, count_candidates))
higher_source_glats = np.zeros((higher_total_wavelengths, count_candidates))

for i,j in enumerate(higher_wavelengths): # Much hardcode. Wow. Very bad practice.
	if j == higher_reference_wavelength:
		higher_source_glons[i,:] = candidate_glons[j]
		higher_source_glats[i,:] = candidate_glats[j]
	else:
		for x in range(count_candidates):
			other_chan = i
			# make arrays of current 350 source to compare to all reference
			# coordinates of candidates
			temp_glon = np.empty(count_candidates)
			temp_glat = np.empty(count_candidates)
			temp_glon.fill(candidate_glons[higher_reference_wavelength][x])
			temp_glat.fill(candidate_glats[higher_reference_wavelength][x])
			# arrays of other source coordinates to compare
			other_source_glon = candidate_glons[j]
			other_source_glat = candidate_glats[j]
			# find distances
			dist = 3600*ang_sep(temp_glon, temp_glat, other_source_glon, other_source_glat)
			# find indicies of all sources within set distance
			same_source = [ind for ind,v in enumerate(dist) if v<=beam]
			num_associated_sources = len(same_source)
			if num_associated_sources != 0:
				# match the closest reference source only to this long wl centroid
				if num_associated_sources == 1:
					higher_source_glons[other_chan, x] = other_source_glon[same_source[0]]
					higher_source_glats[other_chan, x] = other_source_glat[same_source[0]]
				else:
					closest_source = [ind for ind,v in enumerate(dist) if v == np.amin(dist[same_source])]
					higher_source_glons[other_chan, x] = other_source_glon[closest_source[0]]
					higher_source_glats[other_chan, x] = other_source_glat[closest_source[0]]

# store source coordinates by wavelength
higher_candidate_glons = {}
higher_candidate_glats = {}
for x in range(higher_total_wavelengths):
	higher_candidate_glons[higher_wavelengths[x]] = higher_source_glons[x,:]
	higher_candidate_glats[higher_wavelengths[x]] = higher_source_glats[x,:]

# match sources between two runs
# ------------------------------------------------------------------------------
comparison_reference = np.array([candidate_glons[reference_wavelength], candidate_glats[reference_wavelength], candidate_glons[higher_reference_wavelength], candidate_glats[higher_reference_wavelength]])
comparison_higher = np.array([higher_candidate_glons[reference_wavelength], higher_candidate_glats[reference_wavelength], higher_candidate_glons[higher_reference_wavelength], higher_candidate_glats[higher_reference_wavelength]])

matched_inds = []
for higher_source in comparison_higher.T:
	for i,source in enumerate(comparison_reference.T):
		if source.tolist() == higher_source.tolist():
			matched_inds.append(i)
# save indices of candidates that also appear in the higher run
matched_inds = list(set(matched_inds))
# find this in terms of original reference index
print 'Sources found from two merged runs :  ' + str(len(matched_inds))

# update candidates with new indices
candidate_indices = candidate_indices[matched_inds]
for x in wavelengths:
	candidate_glons[x] = candidate_glons[x][matched_inds]
	candidate_glats[x] = candidate_glats[x][matched_inds]
	candidate_dists[x] = candidate_dists[x][matched_inds]
count_candidates = len(candidate_indices)
print 'Just checking that this number is the same: ' + str(count_candidates)

# removal of duplicate sources in output list
# ------------------------------------------------------------------------------
# uses new subset of candidates and compares to same wavelength
print 'Removing duplicate reference sources...'
for x in range(count_candidates):
	temp_glon = np.empty(count_candidates)
	temp_glat = np.empty(count_candidates)
	temp_glon.fill(candidate_glons[reference_wavelength][x])
	temp_glat.fill(candidate_glats[reference_wavelength][x])
	other_source_glon = candidate_glons[reference_wavelength]
	other_source_glat = candidate_glats[reference_wavelength]
	dist = 3600*ang_sep(temp_glon, temp_glat, other_source_glon, other_source_glat)
	same_source = [ind for ind,v in enumerate(dist) if v<=same_wl_beam]
	num_same_source = len(same_source)
	if num_same_source >= 2:
		# this is a duplicate source, destroy this set of coordinates
		candidate_glons[reference_wavelength][x] = 9000
		candidate_glats[reference_wavelength][x] = 9000

# filter out the marked duplicate coordinates
not_a_duplicate = [i for i,v in enumerate(candidate_glons[reference_wavelength]) if v != 9000]
candidate_indices =  candidate_indices[not_a_duplicate]
count_candidates = len(candidate_indices)
for x in wavelengths:
	candidate_glons[x] = candidate_glons[x][not_a_duplicate]
	candidate_glats[x] = candidate_glats[x][not_a_duplicate]
	candidate_dists[x] = candidate_dists[x][not_a_duplicate]
candidate_maps = [single_wl_maps[reference_wavelength][i] for i in candidate_indices]
print 'Final number of sources found:  ' + str(count_candidates)

# catalogue write
# ------------------------------------------------------------------------------
# convert relevant source coords into RA and DEC (J200) for output
candidate_ras = {}
candidate_decs = {}
for x in wavelengths_required:
	source_coords = SkyCoord(SkyCoord(candidate_glons[x]*u.degree, candidate_glats[x]*u.degree, frame='galactic'))
        source_coords = source_coords.transform_to('icrs')
        candidate_ras[x] = source_coords.ra.degree
        candidate_decs[x] = source_coords.dec.degree



col_width = 15
catalogue_out_name = 'python_src_assoc_'
for x in range(total_required):
	catalogue_out_name += str(wavelengths_required[x]) +'_'
catalogue_out_name += str(beam) + 'asec.dat'
catalogue_out_path = output_loc + catalogue_out_name
catalogue_out = open(catalogue_out_path, 'w')
header = ['map name','source', 'band [mu]', 'glon', 'glat', 'ra', 'dec', 'distance ["]']
catalogue_out.write("".join(data.ljust(col_width) for data in header))
catalogue_out.write('\n' + '-'*135 + '\n')

unique_maps = list(unique_everseen(candidate_maps))
for IRDC in unique_maps:
	# indices to use from candidate lists
	sources_in_map = [i for i,v in enumerate(candidate_maps) if v==IRDC]
	# write each candidate with index in sources_in_map
	for number,index in enumerate(sources_in_map):
		# number starts from 0
		# one band at a time for the source
		for wl in wavelengths_required:
			# construct a row to write
			row =[IRDC,str(number+1),str(wl),"{0:.4f}".format(candidate_glons[wl][index]), "{0:.4f}".format(candidate_glats[wl][index]),"{0:.4f}".format(candidate_ras[wl][index]), "{0:.4f}".format(candidate_decs[wl][index]), "{0:.2f}".format(candidate_dists[wl][index])]
			print "".join(data.ljust(col_width) for data in row)
			catalogue_out.write("".join(data.ljust(col_width) for data in row))
			catalogue_out.write('\n')

catalogue_out.close()
