# main.py
# ******************************************************************************
# much development version
# very unprepare
# wow
# such broken variable
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
import coord_tools # conversions between systems and angular separations
import find_reference_sources

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
# send: reference_wavelength map names, coords to find_reference_sources
# return: ammended reference wavelength map names, coords in same format
# NOTE: do other_wavelengths require filtering too?


single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength] = find_reference_sources.duplicate_filter(single_wl_maps[reference_wavelength], glon[reference_wavelength], glat[reference_wavelength], same_wl_beam)



########################
## WORKING UP TO HERE ##
########################


# find counterparts in specified wavelengths
# ------------------------------------------------------------------------------
# send ammended reference_wavelength data with other wavelengths to find_counterparts
# return: coords, distances in each wavelength with reference_wavelength map name
# for all sources with a counterpart in all wavelengths_required and no
# counterpart in wavelengths_excluded

# remove sources with multiple higher resolution sources assigned to one
# lower resolution sources
# ------------------------------------------------------------------------------
# NOTE: Is this necessary?
# NOTE: direct duplicates only- see filtering note regarding further specification

# might run in find_counterparts, or create second run using the longest wavelength
# as temp_reference and finding the closest reference source, only using the
# current subset returned from find_counterparts
# return: coords, distances and reference_wavelength map name as above, with only
# one reference source per longest wavelength source
# -----> see find_counterparts_alpha for existing version

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
