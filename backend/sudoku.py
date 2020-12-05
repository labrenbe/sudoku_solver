from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from backend.solver import solve_sudoku, generator

DEBUG = True

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/solve", methods=["POST"])
def solve():
    matrix = request.json
    blocks, values = split_matrix(matrix)
    solved_matrix = merge_matrix(blocks, solve_sudoku.solve_sudoku(np.array(values), np.array(blocks)).tolist())
    print(matrix, solved_matrix)
    return jsonify(solved_matrix)


@app.route("/generate", methods=["GET"])
def generate():
    return jsonify(merge_matrix(generator.generate_blocks(), generator.generate_sudoku("easy").tolist()))


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


if __name__ == '__main__':
    app.run()
