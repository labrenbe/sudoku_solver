import numpy as np


def update_cand(candidates, curr_field, new_entry, block_members):
    """
    Updates the matrix of possible Sudoku entries
    """
    # Input:
    # - candidates  Old version of the candidate matrix (i.e. 9x9x9 that is to be updated)
    # - curr_field  Coordinates of the field where a new entry was found (row and column)
    # - new_entry   The actual new entry that was found
    # - block_members
    #               All the members of the 9-field block of the current field. These are handed over
    #               as coordinates again
    #
    # Output:
    # - candidates This variable is modified in this function
    #

    # After a field was filled we need to update the candidate matrix
    # Firstly delete all entries for the field just filled
    candidates[curr_field[0], curr_field[1], :] = 0
    # Then update the current row
    candidates[curr_field[0], :, (new_entry - 1)] = 0
    # Update current column
    candidates[:, curr_field[1], (new_entry - 1)] = 0
    # And at last update the current block which is the most tricky
    for j_block in block_members:
        candidates[j_block[0]][j_block[1]][new_entry - 1] = 0