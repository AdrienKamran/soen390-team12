# Paths to the index page are organized here.

from django.urls import path

from sales.views import sales_view, add_sale_order, add_customer
from . import views
from inventory import views as inventoryViews

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginPage, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('generate', views.generateReport, name='generate'),
    path('manufacturing', inventoryViews.manufacturingViewPage, name='manufacturing'),
    path('createmateriallist', inventoryViews.createMaterialList, name='createMaterialList'),
    path('produceMaterialList', inventoryViews.produceMaterialList, name='produceMaterialList'),
    path('manufacture/create-product/', inventoryViews.manufactureProduct, name='manufacture-product'),
    path('inventory', views.inventory, name="inventory"),
    path('inventory/get-raw-material/', views.returnRawMaterial, name='return-raw-material'),
    path('inventory/order-raw-material/', views.orderRawMaterial, name='order-raw-material'),
    path('inventory/create-raw-material/', views.createRawMaterial, name='create-raw-material'),
    path('inventory/check-unique/', views.checkUniqueRawMatName, name='check-unique'),
    path('inventory/get-vendor/', views.returnVendor, name='return-vendor'),
    path('sales', sales_view, name='sales'),
    path('sales/add-customer', add_customer, name='add-customer'),
    path('sales/add-order', add_sale_order, name='add-order')
]
