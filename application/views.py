from django.shortcuts import render
import numpy as np
from django.http import HttpResponse

# Create your views here.
from django.template import loader

from solver_logic.solve_sudoku import solve_sudoku

blocks = np.array([[1, 1, 1, 2, 2, 2, 3, 3, 3],
                   [1, 1, 1, 2, 2, 2, 3, 3, 3],
                   [1, 1, 1, 2, 2, 2, 3, 3, 3],
                   [4, 4, 4, 5, 5, 5, 6, 6, 6],
                   [4, 4, 4, 5, 5, 5, 6, 6, 6],
                   [4, 4, 4, 5, 5, 5, 6, 6, 6],
                   [7, 7, 7, 8, 8, 8, 9, 9, 9],
                   [7, 7, 7, 8, 8, 8, 9, 9, 9],
                   [7, 7, 7, 8, 8, 8, 9, 9, 9]])


def solve(request):
    matrix = np.zeros((9, 9), dtype=int)

    for y in range(9):
        for x in range(9):
            value = request.POST.get(str(y) + ':' + str(x))
            matrix[y][x] = value if value is not None and value != '' else 0

    matrix = solve_sudoku(matrix, blocks)

    return render(request, 'application/sudoku_solver.html', {'matrix': matrix})


def reset(request):
    matrix = np.zeros((9, 9), dtype=int)
    print(matrix)
    return render(request, 'application/sudoku_solver.html', {'matrix': matrix})
