import numpy as np
import numpy.random as ran
import solve_sudoku as ss
import update_cand as uc
import time
def generate_sudoku(difficulty = "easy"):
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

    #Initialize output
    blocks = init_blocks()

    # Define parameters
    # min_initial_numbers   Number of fields allowed in the initial setup
    # allow_branching       0: Every field can be determined straight-forward
    #                       else: Guessing may be necessary
    if difficulty == "easy":
        min_initial_numbers = 60
        allow_branching = 0
    elif difficulty == "medium":
        min_initial_numbers = 40
        allow_branching = 0
    elif difficulty == "hard":
        min_initial_numbers = 30
        allow_branching = 1
    else:
        raise ValueError("In generator.py: Wrong difficulty value, only 'easy', 'medium' and 'hard' are supported.")

    # Generate the entries to be filled in
    new_entries = ran.choice([(i%9)+1 for i in range(81)], min_initial_numbers, replace = False)

    # Now keep looping trough all of the entries and find a position for them all
    # while making sure, that in the end the puzzle is uniquely solvable and fulfills our
    # requirements.
    while True:
        it = 0
        if it >= 100:
            raise ValueError("WARNING: Could not find suitable puzzle after 100 iterations.")

        # Also initialise the sudoku field and a candidate matrix used for number insertion
        puzzle = np.zeros((9, 9), dtype="int")
        cand = np.ones((9, 9, 9), dtype="int")
        # Additionally we create a history being used for possible reverses
        puzzle_history = np.zeros((9,9,min_initial_numbers+1), dtype="int")
        nr_e = 0
        for e in new_entries:
            nr_e += 1
            # Since we want a bit of randomness in here we will not loop through the fields in order:
            for i in np.random.permutation([j for j in range(81)]):
                row = int(i / 9)
                col = i % 9
                block_members = np.transpose(np.nonzero(blocks == blocks[row][col]))

                # Now this is the crucial part: we only add the entry e to field i
                # if we can be sure that it's feasible AND a solution still exists after we add it
                # Otherwise we look at the next field.
                if cand[row][col][e-1] == 1:
                    puzzle[row, col] = e
                    if reqs_fulfilled(puzzle, blocks, allow_branching):
                        uc.update_cand(cand, [row,col], e,block_members)
                        puzzle_history[:,:,nr_e] = puzzle
                        break
                    else:
                        puzzle[row, col] = 0

            # This point is only reached if we did not find a suitable field for entry e
            # in the loop before. That on the other hand means, that we have to take a step
            # back and retry.
            # TODO

        # At this point all numbers should be distributed.
        # If we found a suitable puzzle (i.e. matching all requirements), we have finished
        if reqs_fulfilled(puzzle, blocks, allow_branching):
            break
        it += 1

    return puzzle

def reqs_fulfilled(field, blocks, allow_branching):
    """
    Function that checks if the requirements for the solution are fulfilled.
    """
    # Those are that 1. a solution exists, 2. that this solution is unique
    # and 3. that branching (i.e. guessing) is only necessary as desired.
    # Input:
    #     field   Current standing of the Sudoku
    #     blocks  Blocks of the current Sudoku
    #     allow_branching
    #             Flag that marks if branching is allowed
    # Output:
    #     reqs    Flag indicating if the three criteria mentioned above are fulfilled

    reqs = False
    sol_exist, sol_unique, branching_req = ss.solve_sudoku(field, blocks, generation=True)
    if sol_exist and sol_unique and (branching_req == allow_branching or allow_branching):
        reqs = True
    return reqs

def init_blocks():
    # Little helper function to create the default blocks of a sudoku
    blocks = np.zeros((9,9), dtype="int")

    for i in range(9):
        for j in range(9):
            blocks[i,j] = 1 + 3*np.floor(i/3) + np.floor(j/3)

    return blocks


if __name__ == "__main__":
    # block = init_blocks()

    # print("Expected: 2 and 7 ; Received: {} and {}".format(block[0,3], block[7,0]))
    field = generate_sudoku()

    print(field)