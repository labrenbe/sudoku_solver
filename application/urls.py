from django.urls import path

from . import views

urlpatterns = [
    path('', views.solve, name='solve'),
    path('reset', views.reset, name='reset'),
]