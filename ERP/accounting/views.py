from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
import csv, io

"""
	View for displaying the accunting tab.
"""
@login_required(login_url='login')
def accounting(request):

	# query for fetching all the transactions
	t_query = Transaction.objects.order_by('-t_date').all()

	context = {
		't_query': t_query,
	}

	return render(request, 'accounting.html', context)

@login_required(login_url='login')
def download_accounting_history(request):
    items = Transaction.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction-history.csv"'
    writer = csv.writer(response, delimiter=',')
    #writing attributes
    #Find a way to get the attributes directly from the db
    writer.writerow(['Date', 'Type', 'Name', 'Serial Number', 'Quantity', 'Balance'])

    #writing data corresponding to attributes
    for obj in items:
        writer.writerow([obj.t_date, obj.t_type, obj.t_item_name,  obj.t_serial, obj.t_quantity, obj.t_balance])
    return response
