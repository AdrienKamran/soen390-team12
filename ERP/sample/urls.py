# Paths to the index page are organized here.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginPage, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('generate', views.generateReport, name='generate'),
    path('sales', views.salesViewPage, name='sales'),
    path('manufacturing', views.manufacturingViewPage, name='manufacturing'),
    path('inventory', views.inventory, name="inventory"),
]
