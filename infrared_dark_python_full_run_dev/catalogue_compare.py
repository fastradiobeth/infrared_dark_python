# catalogue_compare.py
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
"""
Tools module for running comparisons between source catalogues
and lists, and writing outputs to files.
Requires: numpy, os, sys
Development plan: enable dual mode functionality
"""

import numpy, os, sys

def matched_sources(compare_A, compare_B):
    """
    Compares columns of arrays based on string characters and returns indices
    of rows in A which also appear in B.
    """
    # matches rows of A and B
    matched_inds = []
    for B_source in compare_B.T:
    	for i,A_source in enumerate(compare_A.T):
    		if A_source.tolist() == B_source.tolist():
    			matched_inds.append(i)
    # save indices of A sources that also appear in the higher run
    matched_inds = list(set(matched_inds))

    return matched_inds

def import_sources(catalogue_path, coord_cols, headerlines=0):
    """
    Imports arrays of glon/ra and glat/dec from a catalogue.
    Requires numpy, os
    """
    if os.path.isfile(catalogue_path) == True:
        x, y = np.loadtxt(catalogue_path, skiprows=headerlines, usecols=coord_cols, unpack=True)
    else:
        sys.exit('Could not find catalogue.')
    return x, y

def find_A_in_B(x_A, y_A, x_B, y_B):
    """
    Returns indicies of sources in catalogue A (x_A, y_A) that have a
    match in catalogue B (x_B, y_B).
    """
    coords_A = np.array([x_A, y_A])
    coords_B = np.array([x_B, y_B])
    not_found_indices = []
    found_indices = []
    for index, source_A in enumerate(coords_A.T):
        instances_matched = 0
        for source_B in coords_B.T:
            if source_B.tolist() == source_A.tolist():
                instances_matched += 1
        if instances_matched > 0:
            # source was matched in B
            found_indices.append(index)
        return found_indices

def find_A_not_in_B(x_A, y_A, x_B, y_B):
    """
    Returns indicies of sources in catalogue A (x_A, y_A) that do not
    have a match in catalogue B (x_B, y_B).
    """
    coords_A = np.array([x_A, y_A])
    coords_B = np.array([x_B, y_B])
    not_found_indices = []
    found_indices = []
    for index, source_A in enumerate(coords_A.T):
        instances_matched = 0
        for source_B in coords_B.T:
            if source_B.tolist() == source_A.tolist():
                instances_matched += 1
        if instances_matched == 0:
            not_found_indices.append(index)
        return not_found_indices

def write_matches(ouput_path, indices, original_path, original_headerlines):
    """
    Writes new catalogue from original_catalogue to ouput_path in same format
    containing only sources with line index in indices.
    """
    original_catalogue = open(original_path, 'r')
    original_lines = original_catalogue.readlines()
    original_header = original_lines[0:headerlines]
    output_catalogue = open(output_path, 'w')
    # adjust indices to account for headerlines in original catalogue
    adjusted_indices = [x+headerlines for x in indices]
    # find correct lines and write
    output_lines = [line for index, line in enumerate(original_lines) if index in adjusted_indices]
    output_catalogue.write(''.join(original_header))
    output_catalogue.write(''.join(output_lines))
    # close catalogues
    output_catalogue.close()
    original_catalogue.close()
    return
