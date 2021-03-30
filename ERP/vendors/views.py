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

# This is the main view that we use to render the vendors.html template
# We provide it with the vendor_pk which allows us to filter the vendor's inventory based on the selected vendor name
# from the dropdown. We also pass in 2 forms; one for creating vendors, and other for Creating/Editing a raw material
# in a given vendor inventory. The last argument we pass to it is a tab to help us navigate between the 3 tabs
# in the vendors module.

@login_required(login_url='login')
def vendors_view(request, vendor_pk=None, vendor_form=None, replenish_form=None, vendors_tab=None):
    if vendors_tab is None:
        tab = 'vendor-register-tab'
    else:
        tab = vendors_tab
    if vendor_form is None:
        vendor_form = VendorForm()
    if replenish_form is None:
        replenish_form = ReplenishMaterialForm()    
    if not vendor_pk is None:
        vendor_inventory = SellsPart.objects.select_related().filter(v_FK=vendor_pk).all()
    else:
        vendor_inventory = SellsPart.objects.select_related().filter(v_FK=0).all()
    vendors = Vendor.objects.all()
    parts = Part.objects.all()      
    context = {
        'vendor_form': vendor_form,
        'replenish_form': replenish_form,
        'vendors': vendors,
        'vendor_inventory': vendor_inventory,
        'parts': parts,
        'tab': tab,
    }    
    return render(request, 'vendors.html', context=context)

# This view is responsible for adding vendors. It accesses the values that are provided in the vendorForm and validate them
# Then saves this new vendor record if it does not exist. if it does exist it adds an error and we print that error
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
            #If the vendor does not exist we create it here
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

# This view is used to filter the inventory of each vendor based on the vendor_id that is passed in the get
# request from the front-end. then it calls the vendors_view and passes it the vendor_id which is used to filter
# the SellsPart model and return all the records for that given vendor_id
@login_required(login_url='login')
def vendors_inventory(request):
    vendor_id = request.GET.get('vendor_id')
    return vendors_view(request, vendor_id, None, None, 'vendor-inventory-tab')

# This view is responsible for deleting a record from the vendor's inventory when a request is made by clicking the minus button
# in the front-end. It takes the pk of the sellsPart record and deletes it and prints a success message.
@login_required(login_url='login')
def delete_item(request):
    sellsPart_pk = request.GET.get('sellsPart_pk') 
    item = SellsPart.objects.filter(pk=sellsPart_pk).first()
    item.delete()
    success = "success"
    messages.success(request, "Items successfully deleted.")
    return JsonResponse(success, safe=False)

# This view is responsible for processing the information that is passed in the replenishMaterialForm
# It validates the values in the form. If a given vendor name and part name already exist in the SellsPart 
# then it updates the current inventory by adding more item quantity to that record
# If a part name does not exist for a given vendor. Then, we create that part in the vendor inventory with the given quantity
@login_required(login_url='login')
def replenish_inventory(request):
    if request.method == 'POST':
        replenish_form = ReplenishMaterialForm(request.POST)
        if replenish_form.is_valid():
            vendor = replenish_form.cleaned_data['vendor']
            part = replenish_form.cleaned_data['part']
            quantity = replenish_form.cleaned_data['quantity']

            #if we don't find a matching record with the same vendor name and  part name in the
            #SellsPart inventory, we create this item for that vendor with a specific quantity
            if not SellsPart.objects.filter(v_FK=vendor, p_FK=part):
                new_item = SellsPart(
                    v_FK=vendor,
                    p_FK=part,
                    p_quantity=quantity
                )
                new_item.save()
                messages.success(request, part.p_name + ' was successfully added to the ' + vendor.v_name + 's inventory')
                return HttpResponseRedirect('/vendors')
            #if we find the part existing in the vendor's inventory, we just add the quantity to the existing one    
            elif SellsPart.objects.filter(v_FK=vendor, p_FK=part):
                selling_part = SellsPart.objects.filter(v_FK=vendor, p_FK=part).first()
                current_quantity = selling_part.p_quantity
                final_quantity = current_quantity + quantity
                selling_part.p_quantity= final_quantity
                selling_part.save()
                messages.success(request, str(quantity) + ' ' + part.p_name + ' item was successfully added to the ' + vendor.v_name + 's inventory')
                return HttpResponseRedirect('/vendors')
        return vendors_view(request, None, None, replenish_form=replenish_form, vendors_tab='vendor-rm-tab')
    return HttpResponseRedirect('/vendors')            