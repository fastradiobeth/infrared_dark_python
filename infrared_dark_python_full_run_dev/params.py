# params.py
# ******************************************************************************
# parameters file required for run of infrared_dark_python
# descriptions may be relocated to man page or other documentation
# ******************************************************************************

# survey setup
# ------------------------------------------------------------------------------
# survey codes:
#   0 - Hi-GAL (use survey_params.py to add more surveys)
survey_code = 0

# survey wavelengths to use
wavelengths = [160,250,350]
wavelengths_required = [250,350]
wavelengths_excluded = [160]
reference_wavelength = 250

# filesystem setup
# ------------------------------------------------------------------------------
# final '/' required for each location string
cat_loc = '/home/beth/Desktop/IRDC_catalogues/' # location of input catalogues
output_loc = '/home/beth/Desktop/' # output location of cutouts
cloud_loc = '/raid/scratch/bjones_IRDC/IRDCs/' # IRDC FITS files location

# MOVE TO CUTOUT SCRIPT
 # TODO: need to make subdirectory in output_loc to store cutouts
output_loc_cutouts = '/raid/scratch/bjones_IRDC/python_src_assoc_250_350_18.0asec_cutouts/'

# single wavelength catalogue setup
# ------------------------------------------------------------------------------

# need to enter a single wavelength catalogue name for each value in 'wavelengths'
single_wl_cats = {
	70 : 'hyper_photometry_sig_var_FWHM_10_new_run_sources_only_70.dat',
	160: 'hyper_photometry_sig_var_FWHM_10_new_run_sources_only_160.dat',
	250: 'hyper_photometry_sig_var_FWHM_10_new_run_sources_only_250.dat',
	350: 'hyper_photometry_sig_var_FWHM_10_new_run_sources_only_350.dat'
}
# single wavelength catalogue settings
map_col = [0]
coord_cols = [2,3]
headerlines = 3
# coord type
#	0	-	Galactic longitude and latitude
#	1	-	RA and DEC (J200)
coord_type = 0


# reference source setup
# ------------------------------------------------------------------------------
# choose settings for removal of duplicate entries/sources closer than a fixed
# distance in reference wavelength source list

# duplicate_filter_type
#	0	-	only remove exact duplicates (default)
#	1 	- 	select survey beam as separation of duplicates (filter_beam)
#	2	-	set fixed separation (fixed_filter)
#	3	- 	use same separation as for counterpart assignment
duplicate_filter_type = 3
filter_beam = 160 # duplicate_filter_type 1 only
fixed_filter = 5 # arcseconds, duplicate_filter_type 2 only


# counterpart association setup
# ------------------------------------------------------------------------------

# separation_type
#	0	- miniumum survey beam of wavelengths_required (default)
#	1	- select a survey beam_to_use as minimum separation
#	2	-  set separation for source association to value of fixed_beam
separation_type = 0
fixed_beam = 5 # arcseconds, separation_type 1 only
beam_to_use = 160 # survey beam, separation_type 2 only


# cutout setup
# ------------------------------------------------------------------------------

# wavelengths of FITS files to cut from
wavelengths_to_cut = [70,160,250,350,500]
# TODO: specify naming of FITS files for import/ glob for them

# codes for cutout width selection
#	0 	-	use maximum angular diameter of starless sources
#	2	- 	set to constant value in degrees, default_cut_width
cut_width_type = 0
default_cut_width = 0.02 # make sure this is the default setting

# catalogue details of starless catalogue, cut_width_type = 0 only
starless_cat_name = 'IRDC_l015_l055_temperature_mass_luminosity_run_160_350.dat'
stl_headerlines = 3
stl_map_col = [0]
stl_rad_and_dist_cols = [4,8]	# source radius in pc and dist in kpc
stl_coord_type = 0
