import numpy as np
import numpy.random as ran
import solve_sudoku as ss
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
    # - init_field       9x9 array containing the starting numbers of the sudoku

    #Initialize output
    init_field = np.zeros((9,9), dtype="int")


    # Generate entries and insert them into the field, checking that it is still viable
    new_entries = ran.choice([(i%9)+1 for i in range(81)], min_initial_numbers, replace = False)

    it = 0
    while True:
        it += 1
        if it > 1000:
            print("WARNING: Could not finish generation - returning current solution!")
            return init_field

        # Generate random fields where the entries are inserted
        indices = ran.choice([i for i in range(81)], min_initial_numbers, replace=False)
        for i in indices:
            row = int(i / 9)
            col = i % 9
            print(row)
            print(col)
            init_field[row, col] = new_entries

        print(init_field)
        time.sleep(0.2)
        # Check for a solution of the sudoku
        sol_exist, sol_unique, branching_req = ss.solve_sudoku(init_field, blocks, generation = True)

        # If we found a suitable field, we have finished
        if sol_exist and sol_unique and (allow_branching or (branching_req == allow_branching)):
            break

    return init_field

def init_blocks():
    # Little helper function to create the default blocks
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