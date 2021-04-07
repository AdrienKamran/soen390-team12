from django.urls import path

from . import views

urlpatterns = [
    path ('', views.vendors_view, name="vendors"), # the default vendor view
    path ('add-vendor/', views.add_vendor, name='add-vendor'), # view to add a new vendor
    path ('vendor-inventory/', views.vendors_inventory, name='vendor-inventory'), # a view that returns the list of items in a given vendor
    path ('delete-inventory-part/', views.delete_item, name='delete-inventory-part'), # ajax endpoint for deleting a items from the vendor inventory
    path ('add-rm/', views.replenish_inventory, name='add-rm'), # view to create/edit a raw material for a given vendor
]