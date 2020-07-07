from django.urls import path

from . import views

urlpatterns = [
    path('', views.solve, name='sudoku_solver'),
]