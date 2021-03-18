# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.manufacturingViewPage, name='manufacturing'),
    path('createmateriallist/', views.createMaterialList, name='createMaterialList'),
    path('produceMaterialList/', views.produceMaterialList, name='produceMaterialList'),
    path('loadMaterialList/', views.loadMaterialList, name='loadMaterialList'),
    path('create-product/', views.manufactureProduct, name='manufacture-product'),
]