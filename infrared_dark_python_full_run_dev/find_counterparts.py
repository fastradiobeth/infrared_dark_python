# find_counterparts
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
"""
Module containing code to associate counterparts to a reference source.
Designed for finding counterparts in other wavelengths using a
catalogue of sources in a reference wavelength.
Required modules: numpy, infrared_dark_python/coord_tools
"""

import numpy as np
import coord_tools

# input: all glat, all glon, reference maps, beam, wavelengths, required_wavelengths, excluded_wavelengths,  reference wavelength
def find_counterparts(single_wl_maps, glon, glat, wavelengths, wavelengths_required, wavelengths_excluded, reference_wavelength, beam):
    """
    Associates counterparts to sources in single wavelength catalogues
    that are passed in as map, glon and glat dictionaries with
    wavelength values as keys. All sources with at least one
    counterpart in all wavelengths_required listed, and no counterparts
    in any wavelengths_excluded.
    Counterparts are associated to a source in the reference_wavelength
    if the centroid is within 1 beam of the reference source centroid.
    Returns candidates with all requirements met by a map list,
    glon in each required wavelength, glat in each required wavelength
    and the distance to an associated centroid in each wavelength.
    """
    total_wavelengths = len(wavelengths)
    total_sources = len(single_wl_maps[reference_wavelength])
    total_required = len(wavelengths_required)

    # set up arrays for storing sources + counterparts
    source_glons = np.zeros((total_wavelengths, total_sources))
    source_glats = np.zeros((total_wavelengths, total_sources))
    source_dists = np.zeros((total_wavelengths, total_sources))
    source_all_wl = np.zeros((total_wavelengths, total_sources))

    # for all wavelengths required to be considered a candidate source
    for i,j in enumerate(wavelengths):
        print 'Associating sources in ' + str(j) + ' microns... \n'
    	if j == reference_wavelength:
    		source_all_wl[i,:] = 1
    		source_glons[i,:] = glon[j]
    		source_glats[i,:] = glat[j]
    	else:
    		for x in range(total_sources):
    			other_chan = i
    			total_other_wl_sources = len(single_wl_maps[j])
    			# make arrays of current 160 source to compare to all other sources
    			temp_glon = np.empty(total_other_wl_sources)
    			temp_glat = np.empty(total_other_wl_sources)
    			temp_glon.fill(glon[reference_wavelength][x])
    			temp_glat.fill(glat[reference_wavelength][x])
    			# make arrays of other sources
    			other_source_glon = glon[j]
    			other_source_glat = glat[j]
    			# find distances
    			dist = 3600*coord_tools.ang_sep(temp_glon, temp_glat, other_source_glon, other_source_glat)
    			# find indicies of all sources within set distance from ref centroid
    			same_source = [ind for ind, v in enumerate(dist) if v<=beam]
    			num_associated_sources = len(same_source)
    			if num_associated_sources != 0:
    				if j in wavelengths_required:
    					# is useful, save details
    					source_all_wl[other_chan, x] = 1
    					if num_associated_sources == 1:
    						# save coordinates of counterpart
    						source_glons[other_chan, x] = other_source_glon[same_source[0]]
    						source_glats[other_chan, x] = other_source_glat[same_source[0]]
    						source_dists[other_chan, x] = dist[same_source[0]]
    					else:
    						# pick closest counterpart and save coordinates
    						closest_source = [ind for ind,v in enumerate(dist) if v == np.amin(dist[same_source])]
    						source_glons[other_chan, x] = other_source_glon[closest_source[0]]
    						source_glats[other_chan, x] = other_source_glat[closest_source[0]]
    						source_dists[other_chan, x] = dist[closest_source[0]]
    				elif j in wavelengths_excluded:
    					# make sure source does not appear in candidates list
    					source_all_wl[other_chan, x] = 800
    				#else:
    					# ignore, not interested in this wavelength
    					# can put extra code here to do something with sources
    					# detected in additional (but not required) wavelengths
    			#else:
    				# do not change entry in indicator array


    # filter lists to contain only sources detected in all wavelengths
    total_wavelengths_observed = source_all_wl.sum(axis=0)
    candidate_indices = [i for i,v in enumerate(total_wavelengths_observed) if v==total_required]
    candidate_indices = np.asarray(candidate_indices)
    # the map assigned to each source is the map of the reference wavelength source
    candidate_maps = [single_wl_maps[reference_wavelength][i] for i in candidate_indices]
    candidate_glons = {}
    candidate_glats = {}
    candidate_dists= {}
    for x in range(total_wavelengths):
    	candidate_glons[wavelengths[x]] = source_glons[x,candidate_indices]
    	candidate_glats[wavelengths[x]] = source_glats[x, candidate_indices]
    	candidate_dists[wavelengths[x]] = source_dists[x, candidate_indices]

    return candidate_maps, candidate_glons, candidate_glats, candidate_dists
