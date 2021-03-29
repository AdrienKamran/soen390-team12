from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

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
def vendors_view(request, vendor_pk=None, vendor_form=None, vendors_tab=None):
    if vendors_tab is None:
        tab = 'vendor-register-tab'
    else:
        tab = vendors_tab
    if vendor_form is None:
        vendor_form = VendorForm()
    if not vendor_pk is None:
        vendor_inventory = SellsPart.objects.select_related().filter(v_FK=vendor_pk).all()
    else:
        vendor_inventory = SellsPart.objects.select_related().filter(v_FK=0).all()
    vendors = Vendor.objects.all()
        
    context = {
        'vendor_form': vendor_form,
        'vendors': vendors,
        'vendor_inventory': vendor_inventory,
        'tab': tab,
    }    
    return render(request, 'vendors.html', context=context)

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

@login_required(login_url='login')
def vendors_inventory(request):
    vendor_id = request.GET.get('vendor_id')
    return vendors_view(request, vendor_id, None, 'vendor-inventory-tab')

@login_required(login_url='login')
def delete_item(request):
    sellsPart_pk = request.GET.get('sellsPart_pk') 
    item = SellsPart.objects.filter(pk=sellsPart_pk).first()
    item.delete()
    test = "success"
    messages.success(request, "Items successfully deleted.")
    return JsonResponse(test, safe=False)   