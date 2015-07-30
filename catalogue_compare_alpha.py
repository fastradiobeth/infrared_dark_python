# catalgoue_compare_alpha.py
## ******************************************************************************
# July 2015
# Beth Jones
# School of Physics and Astronomy | The University of Manchester
# ******************************************************************************
# assesses whether coordinates in catalogue A appear in catalogue B and writes
# catalogues of 'found' and 'not found' catalogue A sources
# foolishly assumes that everything is glat and glon, and the correct wavelength
# coordinates are being compared (and one row = one source)

print 'catalogue_compare_alpha starting up...\n'

cat_loc = '/home/bjones/Documents/IRDC_catalogues/'

catalogue_name_A = 'new_70_cat_python.txt'
headerlines_A = 2
coord_cols_A = [5,6]

catalogue_name_B = 'IRDC_l015_l055_temperature_mass_luminosity_run_70_350.dat'
headerlines_B = 3
coord_cols_B = [9,10]

if os.path.isdir(cat_loc) == False:
	sys.exit('Catalogue directory not found.')

catalogue_A = cat_loc + catalogue_name_A
if os.path.isfile(catalogue_A) == True:
	glon_A, glat_A = np.loadtxt(catalogue_A, skiprows=headerlines_A, usecols=coord_cols_A, unpack=True)
	print 'Catalogue A imported:  '  + catalogue_name_A + '\n'
else:
	sys.exit('Could not find catalogue A. Quitting...')
coords_A = np.array([glon_A, glat_A])
length_A = len(glon_A)

catalogue_B = cat_loc + catalogue_name_B
if os.path.isfile(catalogue_B) == True:
    glon_B, glat_B = np.loadtxt(catalogue_B, skiprows=headerlines_B, usecols=coord_cols_B, unpack=True)
    print 'Catalogue B imported:  ' + catalogue_name_B + '\n'
else:
    sys.exit('Could not find catalogue B. Quitting...')
coords_B = np.array([glon_B, glat_B])
length_B = len(glon_B)

not_found_indices = []
found_indices = []
for index, source_A in enumerate(coords_A.T):
    instances_matched = 0
    # check all coordinates in B for a match to source A
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

# output write - very testing version only
# ------------------------------------------------------------------------------
not_found_catalogue_file = cat_loc +'not_found.dat'
found_catalogue_file = cat_loc + 'found.dat'
original_catalogue = open(catalogue_A, 'r')
original_lines = original_catalogue.readlines()
original_header = original_lines[0:headerlines_A-1]
not_found_catalogue = open(not_found_catalogue_file, 'w')
found_catalogue = open(found_catalogue_file, 'w')

# adjust indices to account for headerlines in original catalogue
adjusted_not_found_indices = [x+headerlines_A for x in not_found_indices]
adjusted_found_indices = [x+headerlines_A for x in found_indices]

not_found_catalogue.write(''.join(original_header))
not_found_catalogue.write(''.join(original_lines[adjusted_not_found_indices]))
found_catalogue.write(''.join(original_header))
found_catalogue.write(''.join(original_lines[adjusted_found_indices]))

not_found_catalogue.close()
found_catalogue.close()
original_catalogue.close()
