from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from dashboard.decorators import *
from .forms import *
from inventory.models import *

import logging

# Create logger
logger = logging.getLogger(__name__)

# Create your views here.

@login_required(login_url='login')
def vendors(request):
    return render(request, template_name='vendors.html', context={})


@login_required(login_url='login')
def vendors_view(request, vendor_form=None):
    if vendor_form is None:
        vendor_form = VendorForm()
    return render(request, 'vendors.html', {'vendor_form' : vendor_form})

@login_required(login_url='login')
def add_vendor(request):
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        if vendor_form.is_valid():           
            vendor_name = vendor_form.cleaned_data.get('v_name')
            vendor_multiplier = vendor_form.cleaned_data.get('v_price_multiplier')
            vendor_address = vendor_form.cleaned_data.get('v_address')
            vendor_city = vendor_form.cleaned_data.get('v_city')
            vendor_province = vendor_form.cleaned_data.get('v_province')
            vendor_zip = vendor_form.cleaned_data.get('v_postal_code')

            if not Vendor.objects.filter(v_name=vendor_name).exists():
                vendor = Vendor(
                    v_name=vendor_name,
                    v_price_multiplier=vendor_multiplier,
                    v_address=vendor_address,
                    v_city=vendor_city,
                    v_province=vendor_province,
                    v_postal_code=vendor_zip,
                )
                vendor.save()
                messages.success(request, vendor_name + ' was created successfully')
                logger.debug("creating vendor with name: " + vendor_name)
                return HttpResponseRedirect('/vendors')
            else:               
                logger.debug("Vendor already exists.")    
        else:
            vendor_form.add_error('v_name', ' Vendor already exists.')
        return vendors_view(request, vendor_form=vendor_form)
    return HttpResponseRedirect('/vendors')