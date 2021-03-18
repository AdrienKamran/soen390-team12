from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction

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
