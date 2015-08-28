# find_reference_sources.py
# ******************************************************************************
# tools for creating single wavelength source lists for counterpart association
# by filtering a single wavelength catalogue to remove duplicate entries and/or
# sources that are too close to be considered as separate objects
# ******************************************************************************

# development version: final part of find_counterparts_alpha used as skeleton
# can be applied to other wavelengths as well as reference if necessary

# input: reference map names, reference glat and glon, same_wl_beam
# output: reference map names, reference glat and glon with duplicates removed
# also needed: angular separation function
# TODO: function use- can import to main and use in all following scripts or import to each individual?
# TODO: run from main as function

# removal of duplicate sources in output list
# ------------------------------------------------------------------------------
# uses new subset of candidates and compares to same wavelength
import coord_tools
import numpy as np

def duplicate_filter(maps, glons, glats, separation = 0):
	source_count = len(maps)
	for x in range(source_count):
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
			glons[x] = 9000
			glats[x] = 9000

	# filter out the marked duplicate coordinates
	not_a_duplicate = [i for i,v in enumerate(glons) if v != 9000]

	# edit arrays to only contain useful sources
	glons = glons[not_a_duplicate]
	glats = glats[not_a_duplicate]
	maps = [maps[i] for i in not_a_duplicate]

	return maps, glons, glats
