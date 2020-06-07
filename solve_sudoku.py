import numpy as np
import init_candidates as initialize
import check_sol as check
import find_new_entry as findnew


def solve_sudoku(init, blocks=np.array([[1, 1, 1, 2, 2, 2, 3, 3, 3],
                                        [1, 1, 1, 2, 2, 2, 3, 3, 3],
                                        [1, 1, 1, 2, 2, 2, 3, 3, 3],
                                        [4, 4, 4, 5, 5, 5, 6, 6, 6],
                                        [4, 4, 4, 5, 5, 5, 6, 6, 6],
                                        [4, 4, 4, 5, 5, 5, 6, 6, 6],
                                        [7, 7, 7, 8, 8, 8, 9, 9, 9],
                                        [7, 7, 7, 8, 8, 8, 9, 9, 9],
                                        [7, 7, 7, 8, 8, 8, 9, 9, 9]])):
    """
    Solves a given Sudoku 
    """
    # Given initial numbers('init') as well as the predefined
    # 9 - number blocks for arbitrary block Sudokus('blocks').
    # Returns the solution also as a 9x9 matrix('solution').
    #
    # Input:
    # - init    Initial Sudoku numbers given in the form of
    #           a 9x9 matrix.
    # - blocks  ~\Optional argument\~ defining 3x3 blocks in
    #           a 9x9 matrix. These should be numbered from
    #           1 to 9. If this argument is not given, a
    #           standard Sudoku is assumed.
    #
    # Output:
    # - solution
    #           Results of the solver again in the form of
    #           a 9x9 matrix

    # Define and initialize variables needed (plus output stuff)
    solution = np.zeros((9, 9), dtype="int")  # Sudoku 9x9 field containing the solution of this solver
    candidates = np.zeros((9, 9, 9), dtype="int")  # Integer array containing the candidates for each field
    solved = 0  # Flag indicating if the Sudoku is fully solved
    new_entry = -1
    found_new_entry = 0  # Flag indicating if the current iteration is finished

    solution = init
    candidates = initialize.init_candidates(init, blocks)

    # Now start the game loop to solve Sudoku
    while solved == 0:
        # First update variables
        found_new_entry = 0
        new_entry = -1

        # First find the empty fields, that still need to be filled
        # The transpose / nonzero combination will return an nx2 array
        # for n empty fields where the first column represents the row
        # and the second one represents the column in the Sudoku field
        empty_field_indices = np.transpose(np.nonzero(solution == 0))

        # Loop through all empty fields to find one to fill
        for curr_field in empty_field_indices:

            # Also determine the current block and its elements
            curr_block = blocks[curr_field[0]][curr_field[1]]
            block_members = np.transpose(np.nonzero(blocks == curr_block))

            # This function checks, if a new entry can be determined
            new_entry, found_new_entry = \
                findnew.find_new_entry(solution, blocks, candidates, curr_field)

            # Fill in the newly found value and update candidate matrix
            if found_new_entry == 1:
                # Fill in the new value
                solution[curr_field[0]][curr_field[1]] = new_entry

                # After a field was filled we need to update the candidate matrix
                # Firstly delete all entries for the field just filled
                candidates[curr_field[0], curr_field[1], :] = 0
                # Then update the current row
                candidates[curr_field[0], :, (new_entry-1)] = 0
                # Update current column
                candidates[:, curr_field[1], (new_entry-1)] = 0
                # And at last update the current block which is the most tricky
                for j_block in block_members:
                    candidates[j_block[0]][j_block[1]][new_entry-1] = 0

                break

        if curr_field[0] >= 0 and curr_field[1] >= 0:
            print("Current standings:")
            print(solution)
            print("Found new value: " + str(new_entry))
            print("At position: (" + str(curr_field[0]) + "/" + str(curr_field[1]) + ")")

        # Guess new entry if no new one was found.
        # If no new entry is found this analytic way we will have
        # to guess one.
        # if found_new_entry == 0:
        #     nr_cand = np.zeros((9, 9), dtype="int")
        #     for i in np.arange(9):
        #         for j in np.arange(9):
        #             nr_cand(i, j) = nnz(candidates(i, j,:))

        # This part just goes to show that we might not be able to solve shit immediately
        if found_new_entry == 0:
            raise ValueError('Could not find a new number! \
                Apparently the solver is too weak ... aborting mission.')

        # Check if we have fully solved the puzzle and the
        # solution is legit
        if (np.count_nonzero(solution) == 81) and \
                (check.check_sol(solution, blocks) == 0):
            solved = 1

    print("*******************************************************")
    print("I have found a complete and correct solution. It reads:")
    print(solution)
