# cutsources_alpha.py
# ******************************************************************************
# July 2015
# Beth Jones
# School of Physics and Astronomy | The University of Manchester
# ******************************************************************************
# cuts out a region around a centroid in IRDC FITS files
# designed for Hi-GAL FITS file naming convention
# standalone code, can be called from main.py usually after assigning counterparts.

print 'Cutsources_alpha.py starting up...'
# header material
# ------------------------------------------------------------------------------
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

# catalogue setup
# ------------------------------------------------------------------------------
# locations of catalogues, IRDCs and output files
cat_loc = '/home/bjones/Documents/IRDC_catalogues/'
cloud_loc = '/raid/scratch/bjones_IRDC/IRDCs/'
output_loc = '/raid/scratch/bjones_IRDC/python_src_assoc_250_350_18.0asec_cutouts/'

# catalogue names and columns of cutout_cat that contain map and coords
cutout_cat_name = 'python_src_assoc_250_350_18.0asec.dat'
cutout_headerlines = 2
map_col =[0]
coord_cols = [3,4]
# for cut_width_type = 1 only
rad_and_dist_cols = []

# catalogue details of starless catalogue for cut_width_type = 0 only
starless_cat_name = 'IRDC_l015_l055_temperature_mass_luminosity_run_160_350.dat'
stl_headerlines = 3
stl_map_col = [0]
stl_rad_and_dist_cols = [4,8]	# source radius in pc and dist in kpc

# parameters for cutout types
# ------------------------------------------------------------------------------
# codes for cut width selection
#	0 	-	use maximum angular diameter of starless sources
#	1	- 	import radius and distance columns from catalogue
#	2	- 	set to constant value in degrees, default value is set here
cut_width_type = 0
default_cut_width = 0.02

# coordinate type codes
#	0 	- 	Galactic longitude and latitude
#	1	- 	RA and DEC (J2000)
coord_type = 0

# wavelengths to cut from
#	 (currently set up for Hi-GAL FITS files)
wavelengths = [70,160,250,350,500]

# check directories
# ------------------------------------------------------------------------------
if os.path.isdir(cat_loc) == False:
	sys.exit('Catalogue directory not found.')
if os.path.isdir(cloud_loc) == False:
	sys.exit('IRDC directory not found.')
if os.path.isdir(output_loc) == False:
	sys.exit('Output directory not found.')

print '\n' + '-'*15 + 'cutsources started' + '-'*15 + '\n'

# import coordinates of maps and sources to be cut
# ------------------------------------------------------------------------------
new_cat = cat_loc + cutout_cat_name
if os.path.isfile(new_cat) == True:
	cutout_maps = (np.loadtxt(new_cat, skiprows=cutout_headerlines, usecols=map_col, dtype=np.str)).tolist()
	glon, glat = np.loadtxt(new_cat, skiprows=cutout_headerlines, usecols=coord_cols, unpack=True)
	print 'Cutout catalogue imported.'
else:
	sys.exit('Could not find cutout catalogue. Quitting...')

total_sources = len(cutout_maps)
print 'Total number of sources to be cut: ' +str(total_sources)

# conversion to angular diameter from radius and distance
# ------------------------------------------------------------------------------
# assumes radius [pc] and distance [kpc]
# uses 1.5*(2*radius) to allow for elliptical sources
def ang_diameter(radius, distance):
	width = np.degrees(np.arctan((1.5*2*radius)/(1000*distance)))
	return width

# selection of cut width
# ------------------------------------------------------------------------------
if cut_width_type == 0:
	# calculate and use maximum starless source width as cut width
	starless_cat = cat_loc + starless_cat_name
	if os.path.isfile(starless_cat) == True:
		starless_maps = (np.loadtxt(starless_cat, skiprows=stl_headerlines, usecols=stl_map_col, dtype=np.str)).tolist()
		rad_stl, dist_stl = np.loadtxt(starless_cat, skiprows=stl_headerlines, usecols=stl_rad_and_dist_cols, unpack=True)
		print 'Starless catalogue imported.'
	else:
		sys.exit('Could not find starless catalogue. Quitting...')

	width_stl = ang_diameter(rad_stl, dist_stl)
	cut_width = max(width_stl)
	cut_width_arr = np.empty(total_sources)
	cut_width_arr.fill(cut_width)
	print 'Cut width set to maximum width of catalogued starless objects:  ' + str(cut_width) + ' deg'

elif cut_width_type == 1:
	radius,distance = np.loadtxt(new_cat, skiprows=cutout_headerlines, usecols=rad_and_dist_cols,  unpack=True)
	cut_width_arr = ang_diameter(radius, distance)

else:
	# set cut width to constant angle in degrees
	cut_width = default_cut_width
	cut_width_arr = np.empty(total_sources)
	cut_width_arr.fill(cut_width)

# cutout code
# ------------------------------------------------------------------------------

for x in range(total_sources):
	cloud_coord = cutout_maps[x]
	if coord_type == 0:
		glon_src = glon[x]
		glat_src = glat[x]
		src_coords = SkyCoord(glon_src*u.degree, glat_src*u.degree, frame='galactic')
		src_coords = src_coords.transform_to('icrs')
		ra_src = src_coords.ra.degree
		dec_src = src_coords.dec.degree
	elif coord_type == 1:
		ra_src = glon[x]
		dec_src = glat[x]

	# loop over wavelegths
	for k in range(len(wavelengths)):
		cloud_name = (cloud_loc + 'HGL' + str(cloud_coord) + '_' + str(wavelengths[k]) + 'mu_J2000.fits')
		output_name = output_loc + 'HGL' + str(cloud_coord) + '_' + str(wavelengths[k]) + 'mu_J2000_cutout_' + '160_quiet_'+str(x) +'.fits'
		montage.commands.mSubimage(cloud_name, output_name, ra_src, dec_src, cut_width_arr[x])
		print str(cloud_coord) + ' single source cut complete in all wls, saved to output_loc.'

print '\n' + '-'*15 +'All cutouts complete.' + '-'*15 + '\n'
