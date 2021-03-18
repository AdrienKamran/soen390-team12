from django.urls import path

from . import views

urlpatterns = [
    path('', views.sales_view, name='sales'),
    path('add-customer/', views.add_customer, name='add-customer'),
    path('add-order/', views.add_sale_order, name='add-order'),
    path('set-order-status/', views.set_order_status, name='set-order-status'),
    ]