# main.py
# ******************************************************************************
# much development version
# very unprepare
# wow
# such broken variable
# ******************************************************************************
# script for running through proccess of associating sources found in single
# wavelengths to sources in other wavelengths and producing FITS cutouts

# TODO: not all of these will be necessary, check
import os
import sys
import glob
import re
import math
import numpy as np
import montage_wrapper as montage
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
from astropy import units as u

# import settings from params.py
# -- TODO: may want to consider only importing relevant variables for given settings
# ---- definitely want to do this
from params import *

# beam selection for counterpart association and duplicate filters
# ------------------------------------------------------------------------------
def wavelength_to_beam(wavelength, survey_code):
    from survey_params import surveys
    survey_beams = surveys[survey_code]
    return survey_beams.get(wavelength)

if separation_type == 1:
    # send to survey params to get beam
	beam = wavelength_to_beam(beam_to_use, survey_code)
elif separation_type == 2:
	# this variable is not a survey param
    beam = fixed_beam
else:
    # send to survey params as for case 1 and find min here.
	total_required = len(wavelengths_required)
	beams = np.empty(total_required)
	for x in range(total_required):    # TODO: for loop probably unecessary, test
		beams[x] = wavelength_to_beam(wavelengths_required[x], survey_code)
	min_beam = np.amin(beams)
	print 'minimum beam: ' + str(min_beam)
	beam = min_beam

# duplicate filter type
if duplicate_filter_type == 1:
	same_wl_beam = wavelength_to_beam(filter_beam, survey_code)
elif duplicate_filter_type == 2:
	same_wl_beam = fixed_filter
elif duplicate_filter_type == 3:
	same_wl_beam = beam
else:
	same_wl_beam = 0


# check for directories and import single wl catalogues
# ------------------------------------------------------------------------------

# filter reference wavelength list subject according to duplicate_filter_type
# ------------------------------------------------------------------------------
# send reference_wavelength map names, coords to find_reference_sources
# return: ammended reference wavelength map names, coords in same format
# NOTE: do other_wavelengths require filtering too?

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
