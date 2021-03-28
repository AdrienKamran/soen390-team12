from django.urls import path

from . import views

urlpatterns = [
    path ('', views.vendors_view, name="vendors"),
    path ('add-vendor/', views.add_vendor, name='add-vendor')
]