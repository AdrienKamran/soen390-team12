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
    path('inventory/get-raw-material/', views.returnRawMaterial, name='return-raw-material'),
    path('inventory/order-raw-material/', views.orderRawMaterial, name='order-raw-material'),
    path('inventory/create-raw-material/', views.createRawMaterial, name='create-raw-material'),
    path('inventory/check-unique/', views.checkUniqueRawMatName, name='check-unique')
]
