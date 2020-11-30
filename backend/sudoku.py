from flask import Flask, jsonify, request
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/solve", methods=["POST"])
def solve():
    matrix = request.json
    matrix[0][0][1] = 1
    blocks, values = split_arrays(matrix)
    return jsonify(matrix)


def split_arrays(matrix):
    blocks = []
    values = []

    for i in range(9):
        for j in range(9):
            blocks[i][j], values[i][j] = matrix[i][j]

    return blocks, values


if __name__ == '__main__':
    app.run()
