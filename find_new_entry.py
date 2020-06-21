import numpy as np


def find_new_entry(field, blocks, candidates, curr_field):
    """
    Checks if a new entry can be uniquely determined
    """
    # Input:
    # - field       Current Sudoku numbers given in the form
    #               of a 9x9 matrix
    # - blocks      Defines the smaller 3x3 blocks in a 9x9
    #               matrix. These should be numbered from 1 to 9.
    # - candidates  Candidate matrix consisting of 9x9x9
    #               integer array with the possible numbers in
    #               each field in the third dimension.
    #               I.e.cand_matrix(x, y, 6) = 1 <= > init(x, y)
    #               is empty and might contain a 6
    # - curr_field  Current field in question. Should contain
    #               row and column in [0] and [1] respectively.
    #
    # Output:
    # - new_entry   This would be the entry found for the field
    #               as an integer.
    # - found_new_entry
    #               Flag indicating if a new entry was actually
    #               found.

    # First of define some necessary values...
    new_entry = -1
    found_new_entry = 0
    irow, icol = curr_field
    # Also determine the current block and its elements
    curr_block = blocks[irow][icol]

    # Little sanity check testing if the field we are looking
    # at right now is actually empty
    if field[irow][icol] != 0:
        raise ValueError('Field is not empty')

    ############################################################
    # This section contains all checks for filling a new field #
    ############################################################
    # 1. Try if there's only one candidate for current field.
    # Therefore check the entries in the candidate  matrix.If
    # only one nonzero entry is found - this is put into the
    # solution.
    if np.count_nonzero(candidates[irow][icol][:]) == 1:
        new_entry = (np.nonzero(candidates[irow][icol][:])[0] + 1)[0]
        found_new_entry = 1
        return new_entry, found_new_entry

    # 2. Try if there is there is a candidate for current field that
    # occurs only once in the current row / column or block
    for new_candidate in range(9):
        if (candidates[irow][icol][new_candidate] == 1) and\
           (np.count_nonzero(candidates[irow, :, new_candidate]) == 1):
            found_new_entry = 1

        if (candidates[irow][icol][new_candidate] == 1) and\
           (np.count_nonzero(candidates[:, icol, new_candidate]) == 1):
            found_new_entry = 1

        temp_cdt = candidates[:, :, new_candidate]
        if (candidates[irow][icol][new_candidate] == 1) and\
           (np.count_nonzero(temp_cdt[blocks == curr_block]) == 1):
            found_new_entry = 1

        if found_new_entry == 1:
            new_entry = new_candidate + 1  # Python is 0-based
            break

    return new_entry, found_new_entry