# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name="inventory"), # default inventory page view
    path('get-raw-material/', views.returnRawMaterial, name='return-raw-material'), # ajax endpoint for returning a raw material
    path('order-raw-material/', views.orderRawMaterial, name='order-raw-material'), # view that orders raw material and redirects back to inventory
    path('create-raw-material/', views.createRawMaterial, name='create-raw-material'), # view to create a raw material
    path('check-unique/', views.checkUniqueRawMatName, name='check-unique'), # ajax endpoint to check if the raw material name is unique
    path('get-vendor/', views.returnVendor, name='return-vendor'), # ajax endpoint that returns a specific vendor object
    path('part/', views.inventoryPartView, name='inventory-part'), # view that displays all parts with a specific part template
    path('toggle-inventory-part-status/', views.toggleInventoryPartStatus, name='toggle-inventory-part-status'), # ajax endpoint to toggle the inventory part status
    path('delete-inventory-part/', views.deleteInventoryPart, name='delete-inventory-part'), # ajax endpoint to delete a part from the inventory
]