# main.py
# ******************************************************************************
# much development version
# very unprepare
# wow
# such module
# ******************************************************************************
# script for running through proccess of associating sources found in single
# wavelengths to sources in other wavelengths and producing FITS cutouts
# TODO: sort out the indentation inconsistency as a result of swapping from Debian
# to Scientific Linux

# packages
# ------------------------------------------------------------------------------
# TODO: not all of these will be necessary, check + write documentation on packages
import os # checked
import sys # checked
import glob
import re # not sure what this is
import numpy as np # checked
#import montage_wrapper as montage   # problems with this (breadstick and almap11) - TODO: check versions of packages and $PATH in both cases

# Beth's modules
import coord_tools, find_reference_sources, find_counterparts, catalogue_compare

# essential parameters
# ------------------------------------------------------------------------------
# import settings from params.py
# -- TODO: may want to consider only importing relevant variables for given settings
# NOTE: NAMESPACES.
from params import survey_code, wavelengths, wavelengths_excluded, wavelengths_required, reference_wavelength, duplicate_filter_type, separation_type, single_wl_cats, map_col, coord_cols, headerlines, coord_type, cat_loc, output_loc


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
	for x in range(total_required):    # TODO: for loop probably unecessary, test
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
# TODO: check cloud locations and created cutout directory when running cutout script
# TODO: check for single_wl_cat existence and exception this

single_wl_maps ={}
dt = np.dtype('f8') # double precision used
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
# NOTE: do other_wavelengths require filtering too?

single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength] = find_reference_sources.duplicate_filter(single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength], same_wl_beam)

# find counterparts in specified wavelengths
# ------------------------------------------------------------------------------
# find all sources with a counterpart in all wavelengths_required and no
# counterpart in wavelengths_excluded

candidate_maps, candidate_glons, candidate_glats, candidate_dists = find_counterparts.find_counterparts(single_wl_maps, glon, glat, wavelengths, wavelengths_required, wavelengths_excluded, reference_wavelength, beam)



# remove sources with multiple higher resolution sources assigned to one
# lower resolution sources
# ------------------------------------------------------------------------------
# NOTE: Is this necessary?
# NOTE: direct duplicates only- see filtering note regarding further specification

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


### TESTING: 160 quiet catalogue reproduction. Gives 840 candidates here. ###
###             -- one less explainable by running duplicate removal first

# print final set of sources to catalogue
# ------------------------------------------------------------------------------
# into output directory (catalogue directory may not have write permissions)

# find all FITS files available for cutting
# ------------------------------------------------------------------------------
# glob cloud_loc for this, and select IRDC FITS files that have map names in
# the written map_names

# cut sources from IRDC FITS
# ------------------------------------------------------------------------------
# send to cutsources: FITS filenames, catalogue maps and all wl coords, output_loc, cutout wavelengths
# return: folder of all FITS cutouts, list of catalogue sources with no IRDC FITS
# file matching its map name
