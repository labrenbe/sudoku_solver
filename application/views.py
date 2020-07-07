from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader

def solve(request):
    context = {}
    for y in range(9):
        for x in range(9):
            cell = str(x) + str(y)
            context[cell] = request.POST.get(cell)
    return render(request, 'application/sudoku_solver.html', context)
