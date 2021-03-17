from django.urls import path

from sales.views import sales_view, add_sale_order, add_customer

urlpatterns = [
    path('', sales_view, name='sales'),
    path('add-customer', add_customer, name='add-customer'),
    path('add-order', add_sale_order, name='add-order')
    ]