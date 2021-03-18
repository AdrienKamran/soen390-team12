# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name="inventory"),
    path('get-raw-material/', views.returnRawMaterial, name='return-raw-material'),
    path('order-raw-material/', views.orderRawMaterial, name='order-raw-material'),
    path('create-raw-material/', views.createRawMaterial, name='create-raw-material'),
    path('check-unique/', views.checkUniqueRawMatName, name='check-unique'),
    path('get-vendor/', views.returnVendor, name='return-vendor'),
    path('part/', views.inventoryPartView, name='inventory-part'),
    path('toggle-inventory-part-status/', views.toggleInventoryPartStatus, name='toggle-inventory-part-status'),
    path('delete-inventory-part/', views.deleteInventoryPart, name='delete-inventory-part'),
]