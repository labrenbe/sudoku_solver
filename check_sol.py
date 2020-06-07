import numpy as np


def check_sol(field, blocks):
    """
    Checks a given Sudoku solution for its correctness
    The field given is checked for correctness.If an error is found the
    type of error is returned.
    """
    # Input:
    #   field   9x9 matrix with integers from 1 to 9 (this won't be checked)
    #           containing the sudoku field blocks this defines the 9-number
    #           blocks inside the 9x9 field (also a 9x9 matrix).Blocks
    #           should be defined from top left to bottom right
    #
    # Output:
    #   result  Integer taking different values for different check results:
    #       -1: An error occured --> check input
    #        0: Current Sudoku solution is legit
    #       1x: First violation in row x
    #       2x: First violation in column x
    #       3x: First violation in block x

    result = -1
    # Now loop through the field checking rows, columns and blocks in one go
    for i in np.arange(9):
        # We have to find the indices of elements which currently belong to
        # the block. Each row in curr_block will contain the row and
        # column of an element belonging to the current block
        curr_block = np.nonzero(blocks == (i+1))

        # These arrays are to check for doubles
        check_doubles_row = np.zeros((9,), dtype=int)
        check_doubles_col = np.zeros((9,), dtype=int)
        check_doubles_block = np.zeros((9,), dtype=int)

        # Now go through each element of the row / column / block to check for
        # doubles
        for j in np.arange(9):
            # Now check for doubles and if they are found return the right error
            # code. Also make sure that no 0 entries are checked
            if (field[i, j] != 0) and (check_doubles_row[field[i, j]-1] == 0):
                check_doubles_row[field[i, j]-1] = 1
            elif (field[i, j] != 0) and (check_doubles_row[field[i, j]-1] != 0):
                # If the field is still zero we do nothing and just continue
                result = 10 + (i+1)

            if (field[j, i] != 0) and (check_doubles_col[field[j, i]-1] == 0):
                check_doubles_col[field[j, i]-1] = 1
            elif field[j, i] != 0 and (check_doubles_col[field[j, i]-1] != 0):
                result = 20 + (i+1)

            # Run through block as well
            curr_val = field[curr_block[0][j], curr_block[1][j]]
            if (curr_val != 0) and (check_doubles_block[curr_val-1] == 0):
                check_doubles_block[curr_val-1] = 1
            elif (curr_val != 0) and (check_doubles_block[curr_val-1] != 0):
                result = 30 + i

    if result == -1:
        result = 0
    return result
