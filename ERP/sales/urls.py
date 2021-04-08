from django.urls import path


from . import views

urlpatterns = [
    path('', views.sales_view, name='sales'), # an endpoint to the default sales view
    path('add-customer/', views.add_customer, name='add-customer'), # an endpoint to the view to add a new customer
    path('add-order/', views.add_sale_order, name='add-order'), # an endpoint to the view to add a new customer
    path('set-order-status/', views.set_order_status, name='set-order-status'), # an endpoint to the view to set order status
    path('download-sales-history-csv/', views.download_sales, name='download-sales'), # an endpoint to export sales history
    ]