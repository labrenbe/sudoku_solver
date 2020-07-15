from django.shortcuts import render
import numpy as np
from django.http import HttpResponse

# Create your views here.
from django.template import loader


def solve(request):
    matrix = np.zeros((9, 9), dtype=int)
    context = {'matrix': matrix}
    for y in range(9):
        for x in range(9):
            value = request.POST.get(str(y) + ':' + str(x))
            matrix[y][x] = value if value != '' else 0
    return render(request, 'application/sudoku_solver.html', context)
