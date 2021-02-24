# Paths to the index page are organized here.

from django.urls import path
from . import views
from inventory import views as inventoryViews

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginPage, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('generate', views.generateReport, name='generate'),
    path('sales', inventoryViews.salesViewPage, name='sales'),
    path('manufacturing', inventoryViews.manufacturingViewPage, name='manufacturing'),
    path('createmateriallist', inventoryViews.createMaterialList, name='createMaterialList'),
    path('inventory', views.inventory, name="inventory"),
]
