# catalogue_compare.py
# tools module for comparing two source lists

def matched_sources(compare_A, compare_B):
    # matches rows of A and B
    matched_inds = []
    for B_source in compare_B.T:
    	for i,A_source in enumerate(compare_A.T):
    		if A_source.tolist() == B_source.tolist():
    			matched_inds.append(i)
    # save indices of A sources that also appear in the higher run
    matched_inds = list(set(matched_inds))

    return matched_inds
