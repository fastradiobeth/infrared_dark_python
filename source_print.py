# source_print.py
# ******************************************************************************
# July 2015
# Beth Jones
# School of Physics and Astronomy | The University of Manchester
# ******************************************************************************
# creates an figure of one IRDC source over all 5 Hi-GAL wavelengths, with a
# large image of the entire IRDC in the reference wavelengths
# assumes naming convention of HGL[map-coords]... for all FITS files and that
# cutouts have been generated using same catalogue (source numbering currently
# requires this, future ammendment to be made here)
import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import aplpy
import matplotlib.pyplot as mpl
from astropy.coordinates import SkyCoord
from astropy import units as u

# select locations of catalogues and FITS files
# ------------------------------------------------------------------------------
cat_loc = '/raid/scratch/bjones_IRDC/'
cloud_loc = '/raid/scratch/bjones_IRDC/IRDC_full_sample/'
cutout_loc = '/raid/scratch/bjones_IRDC/python_src_assoc_70_250_350_10.2asec_2016-06-23/'
output_loc = '/raid/scratch/bjones_IRDC/full_sample_print_format/70_bright'

# setup catalogue
cat_name = 'python_src_assoc_70_250_350_10.2asec_2016-06-23.dat'
new_cat = cat_loc + cat_name

headerlines = 2
map_col = [0]   # map names that match FITS files of IRDCs
coord_wavelengths = [70,250,350]
reference_wavelength = 250
coord_cols = {
    70:[1,2],
    250:[3,4],
    350:[5,6]
}

glat = {}
glon = {}
cutout_maps=np.loadtxt(new_cat, skiprows=headerlines, usecols=map_col, dtype='str')
for x in coord_wavelengths:
    glon[x], glat[x] = np.loadtxt(new_cat, skiprows=headerlines, usecols=coord_cols[x], unpack=True)
total_sources = len(cutout_maps)

# convert all coordinates to ra and dec (J200)
# ------------------------------------------------------------------------------
gal_coords = {}
eq_coords = {}
ra = {}
dec = {}
for w in coord_wavelengths:
    gal_coords[w] = SkyCoord(glon[w], glat[w], frame = 'galactic', unit=(u.degree, u.degree))
    eq_coords[w] = gal_coords[w].transform_to('icrs')
    ra[w] = eq_coords[w].ra.degree
    dec[w] = eq_coords[w].dec.degree

wavelengths = [70, 160, 250, 350, 500]  #Hi-GAL wavelengths
missing_error_count = 0
log_error_count = 0
success_count = 0

# find all available FITS cutouts
cutout_files = glob.glob(cutout_loc+'*.fits')
# find all available IRDCs
cloud_files = glob.glob(cloud_loc+'*.fits')

for x in range(total_sources):
	cutout_names = []
    	# find IRDC FITS file using non-exact catalogue names
	cloud_coord = cutout_maps[x]
	cloud_file_wavelength = '_'+str(reference_wavelength)+'mu_'
	cloud_file_map = 'HGL'+str(cloud_coord)
	matched_clouds = [s for s in cloud_files if cloud_file_map in s]
	matched_ref_cloud = [s for s in matched_clouds if cloud_file_wavelength in s]
   	if len(matched_ref_cloud) !=0:
		cloud_name = matched_ref_cloud[0]
	else:
		cloud_name = 'no_matched_cloud'
	# find IRDC cutout names using non-exact catalogue names
	cutout_index = '_J2000_' + str(x) +'.fits'
	matched_cutouts = [s for s in cutout_files if cutout_index in s]
	print len(matched_cutouts)
	for w in wavelengths:
		cutout_wavelength = '_'+ str(w)+'mu'
  	  	cutout_file_wavelength = [s for s in matched_cutouts if cutout_wavelength in s]
		if len(cutout_file_wavelength) !=0: 
			cutout_names.append(cutout_file_wavelength[0])
		else:
			cutout_names.append('no_matched_file')
   	try:
    		# figure that fits on one landscape A4
     		fig_window = mpl.figure(figsize=(10,7))
     		title = 'Cutouts of [70, 250, 350]micron source with no 160 counterpart from HGL'+ cloud_coord
     		fig_window.suptitle(title, variant='small-caps')
     		cloud_title = 'HGL' + cloud_coord
     		# entire cloud
     		f0 = aplpy.FITSFigure(cloud_name, figure=fig_window, subplot=[0.11,0.5,0.295,0.35])
     		ax = fig_window.gca()
     		ax.set_axis_bgcolor('black')
     		large_label = cloud_title + '\n' + str(reference_wavelength) + '$\mu$m'
     		f0.add_label(0.95,0.85, large_label, color='white', weight='bold', size='x-small', relative=True, horizontalalignment='right')
     		f0.ticks.set_xspacing(0.04)
     		f0.ticks.set_yspacing(0.02)
     		f0.tick_labels.set_xformat('dd.dd')
     		f0.tick_labels.set_yformat('dd.dd')
     		f0.show_colorscale(stretch='log',cmap='gnuplot')
     		f0.axis_labels.set_font(size='small')
     		f0.tick_labels.set_font(size='small')
     		f0.show_markers(ra[reference_wavelength][x], dec[reference_wavelength][x], edgecolor='blue', marker='*')
	
	    	# INDIVIDUAL WAVELENGTHS
	    	# --------------------------------------------------------------------------
	    	# set up standard subplot
	       	marker_colours = {
	            	70:'blue',
       		     	160:'green',
        	    	250:'red',
        	    	350: 'black'
        		}

        	def standard_setup(fig):
            		s=15
    			fig.set_system_latex(True)
    			fig.axis_labels.hide()
        	    	fig.tick_labels.set_xformat('dd.dd')
        	    	fig.tick_labels.set_yformat('dd.dd')
        	    	fig.ticks.set_xspacing=(0.02)
        	    	fig.ticks.set_yspacing=(0.02)
        	    	fig.tick_labels.set_font(size='small')
        	    	fig.show_colorscale(stretch='log', cmap='gnuplot')
    			ax = fig_window.gca()
    			ax.set_axis_bgcolor('black')
        	    	for w in coord_wavelengths:
        	        	fig.show_markers(ra[w][x], dec[w][x], edgecolor=marker_colours[w], s=15)
        	        	s +=2

        	# 70 microns
        	f1 = aplpy.FITSFigure(cutout_names[0], figure=fig_window, subplot=[0.5,0.55,0.195,0.275])
        	standard_setup(f1)
        	f1.add_label(0.95,0.9,'70 $\mu$m', color='white', size='x-small', relative=True, variant='small-caps', horizontalalignment='right')
        	# 160 microns
        	f2 = aplpy.FITSFigure(cutout_names[1], figure=fig_window, subplot=[0.75,0.55,0.195,0.275])
        	standard_setup(f2)
        	f2.tick_labels.hide()
        	f2.add_label(0.95,0.9,'160 $\mu$m', color='white', size='x-small', relative=True, variant='small-caps', horizontalalignment='right')
        	# 250 microns
        	f3 = aplpy.FITSFigure(cutout_names[2], figure=fig_window, subplot=[0.25,0.1,0.195,0.275])
        	standard_setup(f3)
        	f3.tick_labels.hide()
        	f3.add_label(0.95,0.9,'250 $\mu$m', color='white', size='x-small', relative=True, variant='small-caps', horizontalalignment='right')
        	# 350 microns
        	f4 = aplpy.FITSFigure(cutout_names[3], figure=fig_window, subplot=[0.5,0.1,0.195,0.275])
        	standard_setup(f4)
        	f4.tick_labels.hide()
        	f4.add_label(0.95,0.9,'350 $\mu$m', color='white', size='x-small', relative=True, variant='small-caps', horizontalalignment='right')
        	# 500 microns
        	f5 = aplpy.FITSFigure(cutout_names[4], figure=fig_window, subplot=[0.75,0.1,0.195,0.275])
        	standard_setup(f5)
        	f5.tick_labels.hide()
        	f5.add_label(0.95,0.9,'500 $\mu$m', color='white', size='x-small', relative=True, variant='small-caps', horizontalalignment='right')
	
	        # save figure
	        output_name = output_loc + 'HGL' + cloud_coord + '_160_quiet_printing_' + str(x) +'.pdf'
	        fig_window.savefig(output_name)
		success_count +=1
	except IOError:
		print 'Problem finding FITS files for ' + cloud_title + ':  skipping source.... \n'
		missing_error_count +=1
	except Exception:
		print 'Problem setting limits for log scale in ' + cloud_title + ': skipping sources.... \n'
		log_error_count +=1
	
        mpl.close('all')
	
print 'Sources with successful pdf:  ' + str(success_count) + '\n'
print 'Missing file errors:  ' + str(missing_error_count) + '\n'
print 'Log scale display errors:  ' + str(log_error_count) + '\n'
