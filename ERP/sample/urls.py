# Paths to the index page are organized here.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
]
