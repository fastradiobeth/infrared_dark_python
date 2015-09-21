# cutsources.py
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
"""
Tools for setting up required parameters for cutting large numbers of
sources from FITS files and producing the cutouts. Designed for use
with infrared_dark_python scripts.
Required packages: datetime, re, glob, os, numpy, montage_wrapper
Required infrared_dark_python files: coord_tools, params
Note: Working Montage installation is required to use montage_wrapper
"""
import re
import glob
import os
import coord_tools
import numpy as np
import montage_wrapper as montage

def setup(catalogue_name):
    """
    Imports required parameters for cutting sources in catalogue
    catalogue_name to specifications given in params.py. Finds all FITS
    files available for cutting and selects width of cutouts to pass to
    cut(). Also creates output subdirectoy to contain cutout files.
    """
    from params import cloud_loc, cut_width_type
    # find all FITS files present- will include same cloud in multiple bands
    if os.path.isdir(cloud_loc) == False:
        sys.exit('IRDC FITS directory (cloud_loc) not found.')
    # TODO: make this recursive search as different bands may be in subdirectories
    filenames = glob.glob(cloud_loc + '*.fits')
    # make subdirectory in output_loc for cutouts
    cutout_dir = catalogue_name 
    os.mkdir(cutout_dir)

    # select cut width
    # --------------------
    if cut_width_type == 0:
        # calculate and use maximum starless source width as cut width
        from params import starless_cat_name, stl_headerlines, stl_rad_and_dist_cols, cat_loc
        starless_cat = cat_loc + starless_cat_name
        if os.path.isfile(starless_cat) == True:
            rad_stl, dist_stl = np.loadtxt(starless_cat, skiprows=stl_headerlines, usecols=stl_rad_and_dist_cols, unpack=True)
            print 'Starless catalogue imported.'
        else:
            sys.exit('Could not find starless catalogue. Quitting...')
        width_stl = coord_tools.ang_diameter(rad_stl, dist_stl)
        cut_width = max(width_stl)
        print 'Cut width set to maximum width of catalogued starless objects:  ' + str(cut_width) + ' deg'
    else:
        # set cut width to constant angle in degrees
        from params import default_cut_width
        cut_width = default_cut_width

    return cut_width, cutout_dir, filenames


def cut(ra, dec, files, cut_width, input_directory, output_directory, catalogue_index=0):
    """
    Cuts a square region given by the input cut width centred on the
    input coordinates (ra,dec) from all FITS file names provied.
    FITS files (files) are expected to be in the input directory.
    Catalogue index can be used to identify sources when cutouts
    are produced from large catalogues, or defaults to 0 if not given.
    """
    for file in files:
        # name assumes .fits files to remove suffix
        status_name = output_directory + '/' + file[len(input_directory):-5] + '_' + str(catalogue_index) + '.txt'
        output_name = output_directory + '/' + file[len(input_directory):-5] + '_' + str(catalogue_index) + '.fits'
	try:
        	montage.commands.mSubimage(file, output_name, ra, dec, cut_width, status_file=status_name)
	except MontageErorr:
		print 'Sources in ' + file + ' not cut: source outside region'
