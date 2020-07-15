from django.urls import path

from . import views

urlpatterns = [
    path('solve', views.solve, name='solve'),
    path('reset', views.reset, name='reset'),
]