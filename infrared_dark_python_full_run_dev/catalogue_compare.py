# catalogue_compare.py
# tools module for comparing two source lists
"""
Award for Most Underdeveloped Module 2015: currently contains a function
which compares two sets of coordinates (or anything else) to check for
exact string matches. For use with infrared_dark_python_full_run.

Development plan: add the features of catalogue_compare_alpha
to catalogue_compare and enable dual mode functionality of this.
"""

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
