# coord_tools.py
# ******************************************************************************
# various tools to allow for comparison between catalogues
# requires numpy, astropy

import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u

def ang_sep(test_x, test_y, source_x, source_y):
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

def icrs_to_galactic(ra, dec):
	source_coords = SkyCoord(ra*u.degree, dec*u.degree, frame='icrs')
  	source_coords = source_coords.transform_to('galactic')
  	glon = source_coords.l.degree
  	glat = source_coords.b.degree
  	return glon, glat

def galactic_to_icrs(glon, glat):
	source_coords = SkyCoord(glon*u.degree, glat*u.degree, frame='galactic')
	source_coords = source_coords.transform_to('icrs')
	ra = source_coords.ra.degree
	dec = source_coords.dec.degree
	return ra, dec
