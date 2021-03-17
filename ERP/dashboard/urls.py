# Paths to the index page are organized here.

from django.urls import path

from . import views
from inventory import views as inventoryViews
from accounting import views as accountingViews

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginPage, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('generate', views.generateReport, name='generate'),
    path('manufacturing', inventoryViews.manufacturingViewPage, name='manufacturing'),
    path('createmateriallist', inventoryViews.createMaterialList, name='createMaterialList'),
    path('produceMaterialList', inventoryViews.produceMaterialList, name='produceMaterialList'),
    path('loadMaterialList', inventoryViews.loadMaterialList, name='loadMaterialList'),
    path('manufacture/create-product/', inventoryViews.manufactureProduct, name='manufacture-product'),
    path('inventory', views.inventory, name="inventory"),
    path('inventory/get-raw-material/', views.returnRawMaterial, name='return-raw-material'),
    path('inventory/order-raw-material/', views.orderRawMaterial, name='order-raw-material'),
    path('inventory/create-raw-material/', views.createRawMaterial, name='create-raw-material'),
    path('inventory/check-unique/', views.checkUniqueRawMatName, name='check-unique'),
    path('inventory/get-vendor/', views.returnVendor, name='return-vendor'),
    path('inventory/get-vendor/', views.returnVendor, name='return-vendor'),
    path('inventory/part/', views.inventoryPartView, name='inventory-part'),
    path('inventory/toggle-inventory-part-status/', views.toggleInventoryPartStatus, name='toggle-inventory-part-status'),
    path('inventory/delete-inventory-part/', views.deleteInventoryPart, name='delete-inventory-part'),
    path('accounting', accountingViews.accounting, name="accounting"),
]
