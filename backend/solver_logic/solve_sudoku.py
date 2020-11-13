import numpy as np
import time
# from solver_logic import find_new_entry as findnew, check_sol as check, update_cand as update, \
#     init_candidates as initialize
import find_new_entry as findnew, check_sol as check, update_cand as update, \
    init_candidates as initialize

class GameState:
    def __init__(self, field, candidates):
        self.field = field
        self.cand = candidates


def solve_sudoku(init, blocks, generation = False):
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
    # The output of this function is changed with the generation flag!!
    #  Default (generation=False):
    # - solution
    #           Results of the solver again in the form of
    #           a 9x9 matrix
    #  generation=True:
    #   This represents the case when the function is used in generating Sudokus
    #   Hence, we are only interested in some basic information instead of the actual solution:
    #   - sol_exist     Flag indicating if a solution exists
    #   - sol_unique    Flag indicating if the solution is unique (a bit pointless if sol_exist = False)
    #   - branching_needed Flag indicating if the solution is trivial or the solver needed guessing

    # First of all some statistics and timing variables
    # tic = time.perf_counter()
    curr_step = 0

    # Some additional stuff needed for  generation of new Sudokus:
    # Initially we assume that a unique solution exists and we
    # do not require guessing to solve
    if generation:
        sol_exist = False
        sol_unique = True
        branching_needed = False
    else:
        sol_exist = True;sol_unique=True;branching_needed=False

    # Define and initialize variables needed (plus output stuff)
    # solution = np.zeros((9, 9), dtype="int")  # Sudoku 9x9 field containing the solution of this solver
    # candidates = np.zeros((9, 9, 9), dtype="int")  # Integer array containing the candidates for each field
    solved = 0  # Flag indicating if the Sudoku is fully solved
    solution = init
    candidates = initialize.init_candidates(init, blocks)
    state_stack = [GameState(solution, candidates)]

    # Now start the game loop to solve Sudoku
    while solved == 0:
        curr_step += 1
        # First update variables
        found_new_entry = 0
        new_entry = -1
        # Then get the state to be worked on.
        # If state_stack is empty at this point we need to raise an error
        # Most likely the puzzle is unsolvable then
        if state_stack:
            state_work = state_stack.pop()
        else:
            break
        solution = np.copy(state_work.field)
        candidates = np.copy(state_work.cand)

        # Quickly check that we can actually still set new numbers
        # Otherwise we reached a dead end
        if np.count_nonzero(candidates) == 0:
            continue

        # First find the empty fields, that still need to be filled
        # The transpose / nonzero combination will return an nx2 array
        # for n empty fields where the first column represents the row
        # and the second one represents the column in the Sudoku field
        empty_field_indices = np.nonzero(solution == 0)
        empty_field_indices = np.transpose(empty_field_indices)

        # Loop through all empty fields to find one to fill
        for irow, icol in empty_field_indices:
            # Also determine the current block and its elements
            curr_block = blocks[irow][icol]
            block_members = np.transpose(np.nonzero(blocks == curr_block))

            # This function checks, if a new entry can be determined definitively
            new_entry, found_new_entry = \
                findnew.find_new_entry(solution, blocks, candidates, (irow, icol))

            # If we found a new entry we can obviously stop looking
            if found_new_entry == 1:
                break

        # If we have found a new value, update the field and check our new solution
        # Especially for guessing we might obtain wrong solutions here.
        # In that case we forget this path and continue to the next one
        if found_new_entry == 1:
            # Fill in the new value
            solution[irow, icol] = new_entry
            # Update the candidate matrix
            update.update_cand(candidates, (irow,icol), new_entry, block_members)
            solution_valid = check.check_sol(solution, blocks)
            if solution_valid == 0:
                state_stack.append(GameState(solution, candidates))

                # print("Current standings:")
                # print(solution)
                # print("Found new value: " + str(new_entry))
                # print("At position: (" + str(irow) + "/" + str(icol) + ")")
            else:
                # print("Ran into a dead end ...")
                # print(solution_valid)
                # print(solution)
                continue
        # The other case is that we did not find a new entry
        # Then we start the 'guessing game'. Meaning we figure out the
        # field with the least candidates and add all these candidates
        # to the stack of states we still consider
        else:  # found_new_entry == 0
            # Flag to show, that we need branching to solve this one
            if generation:
                branching_needed = True
            # print("NO unique value found starting to branch ...")

            nr_cand = np.count_nonzero(candidates, axis=2)
            # We need to get rid of the zeros ... for reasons
            nr_cand[nr_cand == 0] = 999
            # Find the (first occurence of the) field with the lowest
            # number of candidates
            tmp_index = np.argmin(nr_cand)
            jrow, jcol = np.unravel_index(tmp_index, nr_cand.shape)

            poss_entries = np.array(np.nonzero(candidates[jrow, jcol, :]))
            poss_entries += 1
            # Determine the current block and its elements
            curr_block = blocks[jrow][jcol]
            block_members = np.transpose(np.nonzero(blocks == curr_block))
            for val in np.nditer(poss_entries):
                solution[jrow, jcol] = val
                tmp_candidates = np.copy(candidates)
                update.update_cand(tmp_candidates, (jrow, jcol), val, block_members)
                state_stack.append(GameState(np.copy(solution), tmp_candidates ))

        # Check if we have fully solved the puzzle and the
        # solution is legit
        if (np.count_nonzero(solution) == 81) and \
                (check.check_sol(solution, blocks) == 0):
            # Again more functionality for generation
            if generation:
                # If we come here the first time sol_exist is False
                # --> Set to True, because we now know a solution exists
                if not sol_exist:
                    sol_exist = True
                # If we arrive here again we no that the solution is not unique
                # and stop searching for more solutions
                else:
                    sol_unique = False
                    solved = 1
            else:
                solved = 1

    # toc = time.perf_counter()
    print("*******************************************************")
    print("Found a complete and correct solution. It reads:")
    print(solution)
    if generation:
        return sol_exist,sol_unique,branching_needed
    else:
        return solution
    # print(f"Time needed to solve is {toc-tic:0.4f} seconds.")
    # print(f"It took a whole of {curr_step} steps to obtain.")
