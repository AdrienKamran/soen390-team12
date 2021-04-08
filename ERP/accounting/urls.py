# Paths to the index page are organized here.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.accounting, name="accounting"), # An endpoint for the main accounting view
    path('download-all-csv/', views.download_accounting_history, name='download-accounting-history'), # An endpoint that downloads accounting history
    path('download-profits-csv/', views.download_accounting_profits_history, name='download-accounting-profits-history'), # An endpoint that downloads profits history
    path('download-expenses-csv/', views.download_accounting_expenses_history, name='download-accounting-expenses-history'), # An endpoint that downloads expenses history
]