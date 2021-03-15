from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render
import logging

import json
from django.http import JsonResponse

# Create your views here.
def addCustomer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer-name')
        customer_type = request.POST.get('customer-type')
        customer_email = request.POST.get('customer-email')
        customer_phone_number = request.POST.get('customer-phone-number')
        customer_address = request.POST.get('customer-address')
        customer_province = request.POST.get('customer-province')
        customer_postal = request.POST.get('customer-postal')
        customer_country = request.POST.get('customer-country')
        customer = Customer(name=customer_name, type=customer_type, email=customer_email,
                            phone_number=customer_phone_number, address_line=customer_address, state=customer_province,
                            zip_code=customer_postal, country=customer_country, city='Montreal')
        customer.save()
    return redirect('sales')
