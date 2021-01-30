# Paths to the index page are organized here.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginPage, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('pdf', views.generatePDF, name="pdf"),
    path('csv', views.generateCSV, name="csv"),
]
