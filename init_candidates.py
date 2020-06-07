import numpy as np


def init_candidates(init, blocks):
    """
    Initializes the matrix of possible Sudoku entries
    """
    # Input:
    # - init    Initial sudoku numbers given in the form
    #           of a 9x9 matrix
    # - blocks  Defines the smaller 3x3 blocks in a 9x9 matrix.
    #           These should be numbered from 1 to 9.
    #
    # Output:
    # - cand_matrix
    #           Candidate matrix consisting of a 9x9x9 integer array with
    #           the possible numbers in each field in the third dimension.
    #           I.e.cand_matrix(x, y, 6) = 1 <= > init(x, y) is empty and
    #           might contain a 6.

    # Define Variables
    cand_matrix = np.ones((9, 9, 9), dtype="int")

    # Do the magic
    for i in np.arange(9):
        for j in np.arange(9):
            # If the field is already taken, the respective cand_matrix
            # field set to zero
            if init[i][j] != 0:
                cand_matrix[i][j][:] = 0
                continue
            # If the field is empty we need to look through the respective
            # row / column / block to find all the numbers that can not go
            # into field i, j
            else:
                block_number = blocks[i][j]
                block_fields = init[blocks == block_number]
                # block_fields should always contain 9 elements if the
                # matrix is defined properly

            for k in np.arange(9):
                # We do not really need to check for i / j ~= k here
                # because we already know that init(i, j) == 0.
                # If an element is found the value is now candidate
                # for the current field --> the respective value in
                # the matrix is set to zero.

                # Row
                if init[i][k] != 0:
                    curr_nr = init[i][k]
                    cand_matrix[i][j][curr_nr-1] = 0

                # Column
                if init[k][j] != 0:
                    curr_nr = init[k][j]
                    cand_matrix[i][j][curr_nr-1] = 0

                # Now for the block
                if block_fields[k] != 0:
                    curr_nr = block_fields[k]
                    cand_matrix[i][j][curr_nr-1] = 0

    return cand_matrix

