# find_reference_sources.py
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
"""
Module for filtering lists of sources detected in a single wavelength.
Currently used in infrared_dark_python_full_run for removing duplicate
reference sources.
Required packages: numpy, infrared_dark_python/coord_tools
NOW INCLUDING TIME TESTING
"""

import coord_tools
import numpy as np
import random

def duplicate_filter(maps, glons, glats, separation = 0):
	"""
	Removes duplicate entries of sources in a single wavelength
	catalogue. Separation is 0 by default (only exact duplicates)
	but can be set to a non-zero value [arcseconds] to also remove
	sources with centroids closer together than this separation.
	"""
	source_count = len(maps)
	for x in range(source_count):
		if glons[x] != 9000:
			# arrays containing copies of ONE reference coordinate to check
			temp_glon = np.empty(source_count)
			temp_glat = np.empty(source_count)
			temp_glon.fill(glons[x])
			temp_glat.fill(glats[x])
			# arrays containing the full set of reference sources to compare to
			other_glons = glons
			other_glats = glats
			dist = 3600*coord_tools.ang_sep(temp_glon, temp_glat, other_glons, other_glats)
			# remove all sources subject to same_wl_beam
			same_source = [ind for ind,v in enumerate(dist) if v<=separation]
			num_same_source = len(same_source)
			# will always return at least 1 (compared to self in other_source_glon)
			if num_same_source >= 2:
				# this is a duplicate source, set to invalid coordinates
				# new: randomise which source is kept
				keep_source = random.choice(same_source)
				for index in same_source:
					if index != keep_source:
						# remove all other duplicates
						glons[index] = 9000
						glats[index] = 9000

	# filter out the marked duplicate coordinates
	not_a_duplicate = [i for i,v in enumerate(glons) if v != 9000]

	# edit arrays to only contain useful sources
	glons = glons[not_a_duplicate]
	glats = glats[not_a_duplicate]
	maps = [maps[i] for i in not_a_duplicate]

	return maps, glons, glats
