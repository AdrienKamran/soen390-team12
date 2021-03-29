from django.urls import path

from . import views

urlpatterns = [
    path ('', views.vendors_view, name="vendors"),
    path ('add-vendor/', views.add_vendor, name='add-vendor'),
    path ('vendor-inventory/', views.vendors_inventory, name='vendor-inventory'),
    path ('delete-inventory-part/', views.delete_item, name='delete-inventory-part'),
]