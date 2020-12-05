import numpy as np
import numpy.random as ran


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
    puzzle=np.zeros(81, dtype="int")
    for elems, entry in zip(seed,ran.permutation(9)):
        puzzle[elems]=entry+1
    puzzle = np.reshape(puzzle,(9,9))

    # 2. Rotations of the puzzle do not change the solution so we rotate the field counterclockwise
    #    for random number of times
    puzzle = np.rot90(puzzle,k=ran.choice(4))

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


if __name__ == "__main__":
    field = generate_sudoku()
