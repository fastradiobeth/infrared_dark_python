# catalgoue_compare_alpha.py
## ******************************************************************************
# July 2015
# Beth Jones
# School of Physics and Astronomy | The University of Manchester
# ******************************************************************************
# assesses whether coordinates in catalogue A appear in catalogue B and writes
# catalogues of 'found' and 'not found' catalogue A sources
# assumes compared coordinates are in the same coordinate system and
# one catalogue row = one source

print 'catalogue_compare_alpha starting up...\n'
# header material
# ------------------------------------------------------------------------------
import os
import sys
import numpy as np


# input catalogue parameters
# ------------------------------------------------------------------------------
cat_loc = '/home/bjones/Documents/IRDC_catalogues/'

catalogue_name_A = 'protostellar_extra_all.dat'
headerlines_A = 2
coord_cols_A = [3,4]

catalogue_name_B = 'IRDC_l015_l055_temperature_mass_luminosity_run_160_350.dat'
headerlines_B = 3
coord_cols_B = [9,10]

# read catalogues
# ------------------------------------------------------------------------------
if os.path.isdir(cat_loc) == False:
	sys.exit('Catalogue directory not found.')

catalogue_A = cat_loc + catalogue_name_A
if os.path.isfile(catalogue_A) == True:
	glon_A, glat_A = np.loadtxt(catalogue_A, skiprows=headerlines_A, usecols=coord_cols_A, unpack=True)
	print 'Catalogue A imported:  '  + catalogue_name_A + '\n'
else:
	sys.exit('Could not find catalogue A. Quitting...')
coords_A = np.array([glon_A, glat_A])

catalogue_B = cat_loc + catalogue_name_B
if os.path.isfile(catalogue_B) == True:
    glon_B, glat_B = np.loadtxt(catalogue_B, skiprows=headerlines_B, usecols=coord_cols_B, unpack=True)
    print 'Catalogue B imported:  ' + catalogue_name_B + '\n'
else:
    sys.exit('Could not find catalogue B. Quitting...')
coords_B = np.array([glon_B, glat_B])

# check all coordinates in catalogue A for a match in catalogue B
# ------------------------------------------------------------------------------
not_found_indices = []
found_indices = []
for index, source_A in enumerate(coords_A.T):
    instances_matched = 0
    for source_B in coords_B.T:
        if source_B.tolist() == source_A.tolist():
            instances_matched += 1
    # classify based on number of matches
    if instances_matched == 0:
        # source in A not found in B
        not_found_indices.append(index)
    else:
        # source was matched in B
        found_indices.append(index)

print 'Sources in A found in B:  ' + str(len(found_indices)) + '\n'
print 'Sources in A not found in B:  ' + str(len(not_found_indices)) + '\n'

# write "found" and "not_found" catalogues in format of Catalogue A
# ------------------------------------------------------------------------------
not_found_catalogue_file = cat_loc +'not_found.dat'
found_catalogue_file = cat_loc + 'found.dat'
original_catalogue = open(catalogue_A, 'r')
original_lines = original_catalogue.readlines()
original_header = original_lines[0:headerlines_A]
not_found_catalogue = open(not_found_catalogue_file, 'w')
found_catalogue = open(found_catalogue_file, 'w')

# adjust indices to account for headerlines in original catalogue
adjusted_not_found_indices = [x+headerlines_A for x in not_found_indices]
adjusted_found_indices = [x+headerlines_A for x in found_indices]

not_found_lines = [line for index, line in enumerate(original_lines) if index in adjusted_not_found_indices]
not_found_catalogue.write(''.join(original_header))
not_found_catalogue.write(''.join(not_found_lines))
found_lines = [line for index, line in enumerate(original_lines) if index in adjusted_found_indices]
found_catalogue.write(''.join(original_header))
found_catalogue.write(''.join(found_lines))

not_found_catalogue.close()
found_catalogue.close()
original_catalogue.close()
