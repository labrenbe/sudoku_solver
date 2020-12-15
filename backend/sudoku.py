from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import numpy.random as ran

DEBUG = True

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run()


@app.route("/solve", methods=["POST"])
def solve():
    matrix = request.json
    blocks, values = split_matrix(matrix)
    solved_matrix = merge_matrix(blocks, solve_sudoku(np.array(values), np.array(blocks)).tolist())
    print(matrix, solved_matrix)
    return jsonify(solved_matrix)


@app.route("/generate", methods=["GET"])
def generate():
    return jsonify(merge_matrix(generate_blocks(), generate_sudoku("easy").tolist()))


def split_matrix(matrix):
    blocks = []
    values = []

    for i in range(9):
        blocks.append([])
        values.append([])
        for j in range(9):
            block, value = matrix[i][j]
            if value is None:
                value = 0
            blocks[i].append(block)
            values[i].append(value)

    return blocks, values


def merge_matrix(blocks, values):
    matrix = []
    for i in range(9):
        matrix.append([])
        for j in range(9):
            value = values[i][j]
            if value == 0 or value == '0':
                value = None

            matrix[i].append([blocks[i][j], value])
    return matrix


def update_candidates(candidates, curr_field, new_entry, block_members):
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
    for i in range(9):
        for j in range(9):
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

            for k in range(9):
                # We do not really need to check for i / j ~= k here
                # because we already know that init(i, j) == 0.
                # If an element is found the value is now candidate
                # for the current field --> the respective value in
                # the matrix is set to zero.

                # Row
                if init[i][k] != 0:
                    curr_nr = init[i][k]
                    cand_matrix[i][j][curr_nr - 1] = 0

                # Column
                if init[k][j] != 0:
                    curr_nr = init[k][j]
                    cand_matrix[i][j][curr_nr - 1] = 0

                # Now for the block
                if block_fields[k] != 0:
                    curr_nr = block_fields[k]
                    cand_matrix[i][j][curr_nr - 1] = 0

    return cand_matrix


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
        if (candidates[irow][icol][new_candidate] == 1) and \
                (np.count_nonzero(candidates[irow, :, new_candidate]) == 1):
            found_new_entry = 1

        if (candidates[irow][icol][new_candidate] == 1) and \
                (np.count_nonzero(candidates[:, icol, new_candidate]) == 1):
            found_new_entry = 1

        temp_cdt = candidates[:, :, new_candidate]
        if (candidates[irow][icol][new_candidate] == 1) and \
                (np.count_nonzero(temp_cdt[blocks == curr_block]) == 1):
            found_new_entry = 1

        if found_new_entry == 1:
            new_entry = new_candidate + 1  # Python is 0-based
            break

    return new_entry, found_new_entry


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
    for i in range(9):
        # We have to find the indices of elements which currently belong to
        # the block. Each row in curr_block will contain the row and
        # column of an element belonging to the current block
        curr_block = np.nonzero(blocks == i)

        # These arrays are to check for doubles
        check_doubles_row = np.zeros((9,), dtype=int)
        check_doubles_col = np.zeros((9,), dtype=int)
        check_doubles_block = np.zeros((9,), dtype=int)

        # Now go through each element of the row / column / block to check for
        # doubles
        for j in range(9):
            # Now check for doubles and if they are found return the right error
            # code. Also make sure that no 0 entries are checked
            if (field[i, j] != 0) and (check_doubles_row[field[i, j] - 1] == 0):
                check_doubles_row[field[i, j] - 1] = 1
            elif (field[i, j] != 0) and (check_doubles_row[field[i, j] - 1] != 0):
                # If the field is still zero we do nothing and just continue
                result = 10 + (i + 1)

            if (field[j, i] != 0) and (check_doubles_col[field[j, i] - 1] == 0):
                check_doubles_col[field[j, i] - 1] = 1
            elif field[j, i] != 0 and (check_doubles_col[field[j, i] - 1] != 0):
                result = 20 + (i + 1)

            # Run through block as well
            curr_val = field[curr_block[0][j], curr_block[1][j]]
            if (curr_val != 0) and (check_doubles_block[curr_val - 1] == 0):
                check_doubles_block[curr_val - 1] = 1
            elif (curr_val != 0) and (check_doubles_block[curr_val - 1] != 0):
                result = 30 + i

    if result == -1:
        result = 0
    return result


class GameState:
    def __init__(self, field, candidates):
        self.field = field
        self.candidates = candidates


def solve_sudoku(init, blocks, generation=False):
    """
    Solves a given Sudoku
    """
    # Given initial numbers('init') as well as the predefined
    # 9 - number blocks for arbitrary block Sudokus('blocks').
    # Returns the solution also as a 9x9 matrix('solution').
    #
    # Input:
    # - init    Initial Sudoku numbers given in the form of
    #           a 9x9 matrix. (should be of type np.array)
    # - blocks  ~\Optional argument\~ defining 3x3 blocks in
    #           a 9x9 matrix. These should be numbered from
    #           1 to 9. If this argument is not given, a
    #           standard Sudoku is assumed. (should be an np.array)
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
        sol_exist = True
        sol_unique = True
        branching_needed = False

    # Define and initialize variables needed (plus output stuff)
    # solution = np.zeros((9, 9), dtype="int")  # Sudoku 9x9 field containing the solution of this solver
    # candidates = np.zeros((9, 9, 9), dtype="int")  # Integer array containing the candidates for each field
    solved = 0  # Flag indicating if the Sudoku is fully solved
    solution = init
    candidates = init_candidates(init, blocks)
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
        candidates = np.copy(state_work.candidates)

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
                find_new_entry(solution, blocks, candidates, (irow, icol))

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
            update_candidates(candidates, (irow,icol), new_entry, block_members)
            solution_valid = check_sol(solution, blocks)
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
                update_candidates(tmp_candidates, (jrow, jcol), val, block_members)
                state_stack.append(GameState(np.copy(solution), tmp_candidates ))

        # Check if we have fully solved the puzzle and the
        # solution is legit
        if (np.count_nonzero(solution) == 81) and \
                (check_sol(solution, blocks) == 0):
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
    if generation:
        return sol_exist, sol_unique, branching_needed
    else:
        print("*******************************************************")
        print("Found a complete and correct solution. It reads:")
        print(solution)
        return solution
    # print(f"Time needed to solve is {toc-tic:0.4f} seconds.")
    # print(f"It took a whole of {curr_step} steps to obtain.")


def generate_sudoku(difficulty="easy"):
    """
    Generates a Sudoku with a given difficulty
    """
    # Generates a Sudoku with a given difficulty
    # For now only standard Sudokus with 3x3 subblocks are
    # supported.
    #
    # Input:
    # - difficulty  String specifying the difficulty of the Sudoku to be generated.
    #               Supported values: "easy", "medium", "hard"
    #
    # Output:
    # - puzzle       9x9 array containing the starting numbers of the sudoku

    # Define seed
    # Here we define the seed which is a definitive valid
    # initial solution on which we will later perform
    # random permutations do generate different solutions
    # As you can see the seed is defined as if the puzzle was 1D with columns before rows ...
    # TODO: Create more seeds for different difficulties and randomly select one
    if difficulty == "easy":
        seed = [[20, 40, 55, 69], [12, 31, 51], [35, 61, 76], [53, 59, 65, 78], [19, 27, 66, 74], [2, 28, 42, 48, 70],
                [4, 24, 47, 63, 79], [18, 43, 62, 68, 73], [0, 16, 23, 33, 56]]
    elif difficulty == "medium":
        pass
    elif difficulty == "hard":
        pass
    else:
        raise ValueError("In generator.py: Wrong difficulty value, only 'easy', 'medium' and 'hard' are supported.")

    # Now with a seed loaded we create the randomized Sudoku setup in three steps:
    # 1. It does not matter which number we put where - the Sudoku will always stay feasible
    #    Hence we assign the fields of the seed with a random permutation of the numbers from 1 to 9
    #    Initially the newly generated puzzle is treated as 1D for simplicity.
    puzzle = np.zeros(81, dtype="int")
    for elems, entry in zip(seed, ran.permutation(9)):
        puzzle[elems] = entry + 1
    puzzle = np.reshape(puzzle, (9, 9))

    # 2. Rotations of the puzzle do not change the solution so we rotate the field counterclockwise
    #    for random number of times
    puzzle = np.rot90(puzzle, k=ran.choice(4))

    # 3. Flip the puzzle in left/right and/or up/down direction does also not change the solution
    if ran.choice([False, True]):
        puzzle = np.fliplr(puzzle)
    if ran.choice([False, True]):
        puzzle = np.flipud(puzzle)

    # Return the result
    return puzzle


def generate_blocks():
    return [[0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4, 5, 5, 5],
            [3, 3, 3, 4, 4, 4, 5, 5, 5],
            [3, 3, 3, 4, 4, 4, 5, 5, 5],
            [6, 6, 6, 7, 7, 7, 8, 8, 8],
            [6, 6, 6, 7, 7, 7, 8, 8, 8],
            [6, 6, 6, 7, 7, 7, 8, 8, 8]]



