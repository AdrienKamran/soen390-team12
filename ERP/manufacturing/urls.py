# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.manufacturingViewPage, name='manufacturing'), # default manufacturing view
    path('createmateriallist/', views.createMaterialList, name='createMaterialList'), # url endpoint that creates a material list
    path('produceMaterialList/', views.produceMaterialList, name='produceMaterialList'), # url endpoint for producing a materia list for the front end
    path('loadMaterialList/', views.loadMaterialList, name='loadMaterialList'), # url endpoint for loading an existing material list
    path('create-product/', views.manufactureProduct, name='manufacture-product'), # url endpoint for creating/manufacturing a product/part.
    #path('download-manufacturing-history-csv')
]