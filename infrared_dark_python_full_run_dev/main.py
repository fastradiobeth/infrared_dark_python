# main.py
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
# script for running through proccess of associating sources found in single
# wavelengths to sources in other wavelengths and producing FITS cutouts
"""
Main script for associating counterparts to sources in a reference wavelength
to produce a multi-wavelength catalogue of sources, and optionally creating
cutouts of these sources from larger FITS files of region.
All user input parameters required for the run are found in 'params',
whilst all survey parameters are located in 'survey_params'. No
other files need changing for a full run.

Modules and packages required:
--------------------------------------------------------------------
PACKAGES:
        - datetime, glob, os, re, sys
        - astropy
        - montage_wrapper (cutouts only)
        - more_itertools
        - numpy
    [Note: if cutout option is selected, a working installation of
    Montage is required. This code was tested using Montage v3.3]

IRDP MODULES:
        - catalogue_compare
        - coord_tools
        - cutsources
        - find_counterparts
        - find_reference_sources
        - params
        - survey_params
    [from github.com/fastradiobeth/infrared_dark_python]


Method used:
--------------------------------------------------------------------

0 -  read catalogues and import coordinates, other parameter setup

1 -	Removal of duplicate sources in the reference wavelength
			Uses 'find_reference_sources' module
            Filters the single wavelength catalogue sources to remove
            duplicate sources in the catalogue (exact duplicates or closer
            than specified angular separation)

2 -	Source association by centroids
 			Uses 'find_counterparts' module
            Loops over each source in the filtered reference wavelength
            catalogue and compares to another single wavelength catalogue,
            assigning a counterpart in the other wavelength if a centroid
            in this catalogue is within a specified angular radius.
            If more than one counterpart is identified, the counterpart
            closest to the reference centroid is chosen. Only sources with
            a counterpart found in all required wavelengths are returned.

3 -	Removal of several reference sources assigned to same counterpart
			Uses find_counterparts and catalogue_compare modules
            Only uses sources in the candidate list returned from 2,
            and creates second catalogue of sources using the longest
            wavelength (assumed lowest resolution) and reference
            wavelength centroids. This selects one reference source
            per longest wavelength source, and sources with
            reference+longest wavelength centroids appearing in both
            catalogues are saved.

4 - Catalogue output to output directory
            Writes the final multiwavelength catalogues
            i) Concise version with the IRDC map name assigned to the
            reference centroid with the centroid coordinates of all
            counterterpart in (glon,glat) in order of ascending wavelength
            per line
            ii) Full version with one line per counterpart per source,
            with map name, source number in map in current catalogue,
            (glon,glat) centroid coords, (ra,dec) icrs centroid coords,
            and distance to reference centroid (")

5 - Cutout creation (optional)
            Uses cutsources module
            Finds all available IRDC maps for cutting, and cuts all
            sources in multiwavelength catalogue from matched maps to
            a region of specfied angular diameter around reference
            centroid.
"""
print('\nStarting up...\n')

# packages
# ------------------------------------------------------------------------------
import os
import sys
import re
import datetime
import numpy as np
from more_itertools import unique_everseen

# infrared_dark_python modules
import coord_tools, find_reference_sources, find_counterparts, catalogue_compare, cutsources

# essential parameters
# ------------------------------------------------------------------------------
from params import survey_code, wavelengths, wavelengths_excluded, wavelengths_required, reference_wavelength, duplicate_filter_type, separation_type, single_wl_cats, map_col, coord_cols, headerlines, coord_type, cat_loc, output_loc, want_cutouts

print '\n' + '-'*15 + 'infrared dark python started' + '-'*15 + '\n'

# beam/separation selection
# ------------------------------------------------------------------------------
def wavelength_to_beam(wavelength, survey_code):
    import survey_params
    survey_beams = survey_params.surveys[survey_code]
    return survey_beams.get(wavelength)

if separation_type == 1:
    # send to survey params to get beam
    from params import beam_to_use
    beam = wavelength_to_beam(beam_to_use, survey_code)
elif separation_type == 2:
	# this variable is not a survey param
    from params import fixed_beam as beam
else:
    # use survey_params to select minimum beam
	total_required = len(wavelengths_required)
	beams = np.empty(total_required)
	for x in range(total_required):
		beams[x] = wavelength_to_beam(wavelengths_required[x], survey_code)
	min_beam = np.amin(beams)
	beam = min_beam

# duplicate filter type for find_reference_sources
if duplicate_filter_type == 1:
    from params import filter_beam
    same_wl_beam = wavelength_to_beam(filter_beam, survey_code)
elif duplicate_filter_type == 2:
    from params import fixed_filter as same_wl_beam
elif duplicate_filter_type == 3:
	same_wl_beam = beam
else:
	same_wl_beam = 0

# check for directories and import single wl catalogues
# ------------------------------------------------------------------------------
if os.path.isdir(cat_loc) == False:
	sys.exit('Catalogue directory not found.')
if os.path.isdir(output_loc) == False:
	sys.exit('Output directory not found.')

single_wl_maps ={}
dt = np.dtype('f8') # double precision
glat = {}
glon = {}
if coord_type == 1:
	ra = {}
	dec ={}

for x in wavelengths:
    #TODO: check for any errors when reading in files
    cat_name = cat_loc + single_wl_cats[x]
    single_wl_maps[x] = (np.loadtxt(cat_name, skiprows=headerlines, usecols=map_col, dtype=np.str)).tolist()
    if coord_type == 0:
        glon[x], glat[x] = np.loadtxt(cat_name, skiprows=headerlines, usecols=coord_cols, unpack=True, dtype=dt)
    elif coord_type == 1: # this is unacceptable, make them glat and glon
        ra[x], dec[x] = np.loadtxt(cat_name, skiprows=headerlines, usecols=coord_cols, unpack=True, dtype=dt)
        glon[x], glat[x] = coord_tools.icrs_to_galactic(ra[x],dec[x])
    else:
        sys.exit('Unknown input coordinate type, quitting...')

total_wavelengths = len(wavelengths)
total_required = len(wavelengths_required)
total_sources = len(single_wl_maps[reference_wavelength])

# filter reference wavelength list subject according to duplicate_filter_type
# ------------------------------------------------------------------------------
# TODO: do other_wavelengths require filtering too?
print 'Creating filtered reference source list... \n'
single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength] = find_reference_sources.duplicate_filter(single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength], same_wl_beam)
print 'Number of reference sources:  ' + str(len(single_wl_maps[reference_wavelength])) +'\n'

# find counterparts in specified wavelengths
# ------------------------------------------------------------------------------
# find all sources with a counterpart in all wavelengths_required and no
# counterpart in wavelengths_excluded
print 'Finding counterparts...\n'
candidate_maps, candidate_glons, candidate_glats, candidate_dists = find_counterparts.find_counterparts(single_wl_maps, glon, glat, wavelengths, wavelengths_required, wavelengths_excluded, reference_wavelength, beam)
print 'Number of sources found in all wavelengths:  ' + str(len(candidate_maps)) + '\n'

# remove sources with multiple higher resolution sources assigned to one
# lower resolution sources
# ------------------------------------------------------------------------------
# NOTE: direct duplicates only- see filtering note regarding further specification

print 'Removing duplicates...\n'
# using the current candidate list:
# produce find counterparts_run with longest wl as ref, and then run through
# your *new* (non-existent) catalogue comparison module
longest_wavelength = max(wavelengths_required)
temp_wavelengths_required = [reference_wavelength, longest_wavelength]
temp_wavelengths_excluded = []
temp_candidate_maps = {
    reference_wavelength:candidate_maps,
    longest_wavelength:candidate_maps
}

temp_maps, temp_glons, temp_glats, temp_dists = find_counterparts.find_counterparts(temp_candidate_maps, candidate_glons, candidate_glats, temp_wavelengths_required, temp_wavelengths_required, temp_wavelengths_excluded, longest_wavelength, beam)

# create arrays for rows to be matched
comparison_A = np.array([candidate_glons[reference_wavelength], candidate_glats[reference_wavelength], candidate_glons[longest_wavelength], candidate_glats[longest_wavelength]])
comparison_B = np.array([temp_glons[reference_wavelength], temp_glats[reference_wavelength], temp_glons[longest_wavelength], temp_glats[longest_wavelength]])

# return indices of candidate_glons appearing in both runs
candidate_indices = catalogue_compare.matched_sources(comparison_A, comparison_B)

candidate_maps = [candidate_maps[i] for i in candidate_indices]
for x in wavelengths:
    candidate_glons[x] = candidate_glons[x][candidate_indices]
    candidate_glats[x] = candidate_glats[x][candidate_indices]
    candidate_dists[x] = candidate_dists[x][candidate_indices]

total_candidates = len(candidate_maps)
### TESTING: 160 quiet catalogue reproduction. Gives 840 candidates here. ###
###             -- one less explainable by running duplicate removal first

print 'Total candidates found:  ' + str(total_candidates) + '\n'

# print final set of sources to catalogue
# ------------------------------------------------------------------------------
# into output directory (catalogue directory may not have write permissions)
print 'Writing catalogues...\n'
# convert all coordinates to ra and dec
candidate_ras = {}
candidate_decs = {}
for x in wavelengths_required:
    candidate_ras[x], candidate_decs[x] = coord_tools.galactic_to_icrs(candidate_glons[x], candidate_glats[x])

# setup
col_width = 15
catalogue_out_name = output_loc + 'python_src_assoc_'
for x in wavelengths_required:
    catalogue_out_name += str(x)+'_'
catalogue_out_name += str(beam)+'asec_' + str(datetime.date.today())
catalogue_out_full_path = catalogue_out_name + '_full.dat'
catalogue_out_path = catalogue_out_name + '.dat'

catalogue_header = ['map name']
for x in range(total_required):
	catalogue_header.append(str(wavelengths_required[x]) + ' glon')
	catalogue_header.append(str(wavelengths_required[x]) + ' glat')

catalogue_header_full = ['map name','source', 'band [mu]', 'glon', 'glat', 'ra', 'dec', 'distance ["]']

# write to concise catalogue file
catalogue_out = open(catalogue_out_path, 'w')
catalogue_out.write("".join(data.ljust(col_width) for data in catalogue_header))
catalogue_out.write('\n' + '-'*135 + '\n')
for x in range(total_candidates):
	row = [candidate_maps[x]]
	for wl in wavelengths_required:
		row.append("{0:.4f}".format(candidate_glons[wl][x]))
		row.append("{0:.4f}".format(candidate_glats[wl][x]))
	catalogue_out.write("".join(data.ljust(col_width) for data in row))
	catalogue_out.write('\n')
catalogue_out.close()

# write to full catalogue file
# extra loops are for numbering sources within clouds
catalogue_out = open(catalogue_out_full_path, 'w')
catalogue_out.write("".join(data.ljust(col_width) for data in catalogue_header_full))
catalogue_out.write('\n' + '-'*135 + '\n')
unique_maps = list(unique_everseen(candidate_maps))
for IRDC in unique_maps:
	# indices to use from candidate lists
	sources_in_map = [i for i,v in enumerate(candidate_maps) if v==IRDC]
	# write each candidate with index in sources_in_map
	for number,index in enumerate(sources_in_map):
		# number starts from 0- correct so starts from 1
		# one band at a time for the source
		for wl in wavelengths_required:
			# construct a row to write- no spaces are to prevent syntax highlighting from breaking, sorry
			row=[IRDC,str(number+1),str(wl),"{0:.4f}".format(candidate_glons[wl][index]),"{0:.4f}".format(candidate_glats[wl][index]),"{0:.4f}".format(candidate_ras[wl][index]),"{0:.4f}".format(candidate_decs[wl][index]),"{0:.2f}".format(candidate_dists[wl][index])]
			catalogue_out.write("".join(data.ljust(col_width) for data in row))
			catalogue_out.write('\n')
catalogue_out.close()

# cutouts
# ------------------------------------------------------------------------------
from params import cloud_loc
if want_cutouts == 1:
    print 'Creating cutouts...\n'
    no_file = 0
    multiple_cloud = 0
    cut_width, cutout_dir, filenames = cutsources.setup(catalogue_out_name)
    # need to match coordinate substrings in FITS filenames to candidate_maps
    for i,map_coord in enumerate(candidate_maps):
        # if map coodinate has FITS files, cut source from all FITS files of IRDC
        map_coord_file = 'HGL'+ map_coord
	matched_files = [s for s in filenames if map_coord_file in s]
        if len(matched_files) != 0:
            cutsources.cut(candidate_ras[reference_wavelength][i], candidate_decs[reference_wavelength][i], matched_files, cut_width, cloud_loc, cutout_dir, i)
            if len(matched_files) > 5:
		multiple_cloud +=1
	else:
            # catalogue source FITS file not found, put on some list somewhere or sth
            no_file +=1
	    print 'Source in IRDC at ' + map_coord + ' not cut (no matching FITS file).'
else:
    print 'No cutouts produced'

print 'Number of sources with no matching IRDC FITS file:  ' + str(no_file)
print 'Number of sources with multiple IRDC FITS files matched:  ' +str(multiple_cloud)
print '\n' + '-'*15 + 'infrared dark python done!' + '-'*15 + '\n'
