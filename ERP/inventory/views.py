from django.shortcuts import render, redirect 
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from manufacturing.models import *
from inventory.models import *
from inventory.forms import *
from sales.models import *
from dashboard.decorators import *
from sales.forms import *
from accounting.models import *
from datetime import datetime
from decimal import Decimal
import logging
import io
import csv
import json
from reportlab.pdfgen import canvas

"""
    View that displays the default inventory page
"""
@login_required(login_url='login')
def inventory(request):
    # this takes care of generating all the information for the inventory view.
    context = {}
    if request.method == 'GET':
        # ignore POST requests for this view

        # filter for distinct values of the tuple warehouse and part.
        # eg. A part template will show only once for the same warehouse, but more than once
        # if in different warehouses.
        part_inventory = Contain.objects.select_related().filter(p_in_inventory=True).distinct('p_FK', 'w_FK') # inventory of the different part types in each warehouse
        raw_material_all = Part.objects.filter(p_type='Raw Material').all() # list of all the raw materials in the parts list
        warehouse_all = Warehouse.objects.all() # list of all the warehouses
        vendor_all = Vendor.objects.all() # list of all the vendors
        orders = Order.objects.select_related().all().order_by('timestamp') # list of all the orders
        date_of_day = datetime.now() # today's datetime
        User = get_user_model()
        users = User.objects.all()

        # for every part in the list, find how many of those parts exist in the warehouse and save in a dictionary to be
        # accessible in the inventoy template
        part_inventory_count = {}
        for part in part_inventory:
            # get the length of the array returned by the query
            part_inventory_count[part.p_serial] = len(Contain.objects.filter(p_FK=part.p_FK, w_FK=part.w_FK, p_in_inventory=True).all())
        context = {
            'inventory': part_inventory,
            'inventory_count': part_inventory_count,
            'raw_material_all': raw_material_all,
            'warehouse_all': warehouse_all,
            'vendor_all': vendor_all,
            'rm_orders': orders,
            'date_of_day': date_of_day,
            'users': users
        }
    return render(request, 'inventory.html', context=context) # render the view

"""
    View that handles the ordering of raw material. It processes the information passed inside the POST method and
    redirects to the inventory view with either a success or error message

    Information about the raw material order is passed through the POST request, it is then translated into a form.
    The form is validated and the new order is created.
    A transaction of the order is also created for the accounting tab and for every unit ordered (quantity), a Contain record
    is created to keep track of individual parts in each warehouse.
"""
@login_required(login_url='login')
def orderRawMaterial(request):
    if request.method == 'POST':
        # only handle POST requests at this url endpoint

        # Use form to validate information automatically
        cost = Decimal(request.POST.get('total-cost'))
        cost_rounded = round(cost, 2)
        # pass information to form
        form = OrderRawMaterialForm(data={
            'v_FK': request.POST.get('purchase-vendor-pk'),
            'w_FK': request.POST.get('warehouse-pk'),
            'p_FK': request.POST.get('raw-mat-pk'),
            'order_quantity': request.POST.get('purchase-order-quantity'),
            'order_total_cost': cost_rounded
        })
        # check if form is valid before processing information
        if form.is_valid():
            # save the new record
            new_order = form.save()
            new_order.order_status = 'RECEIVED'
            new_order.save()
            # for the sake of this sprint, the order is automatically shipped and appears in the warehouse inventory

            # get the last serial number for the transactions and increase by one. If no prior transactions exist, default to 500000
            t_last_index_object = Transaction.objects.order_by('-t_serial').first()
            t_last_index = 0
            if t_last_index_object is None:
                t_last_index = 500000
            else:
                t_last_index = t_last_index_object.t_serial + 1

            # create an ORDER transaction
            new_transaction = Transaction(t_type='ORDER', t_balance=-cost_rounded, t_item_name=new_order.p_FK.p_name, t_serial=t_last_index, t_quantity=new_order.order_quantity)
            new_transaction.save()
        
            # before adding the new parts, query the contains list for the last index/serial number.
            last_index_object = Contain.objects.order_by('-p_serial').first()
            last_index = 0
            if last_index_object is None:
                last_index = 10000
            else:
                last_index = last_index_object.p_serial
            i = 0

            # loop for every ordered material and create a record in the inventory
            while i < int(request.POST.get('purchase-order-quantity')):
                # increase serial number by 1
                last_index = last_index + 1
                # create new inventory record
                new_rm = Contain(p_FK=new_order.p_FK, w_FK=new_order.w_FK, p_serial=last_index, p_defective=False, p_in_inventory=True)
                new_rm.save()
                # add the new inventory record to the OrdersPart table to keep track of the specific parts in this order.
                new_order_part = OrdersPart(o_FK=new_order, c_FK=new_rm)
                new_order_part.save()
                i = i + 1

            # Remove the ordered raw materials from the vendors' inventory
            raw_material_pk = request.POST.get('raw-mat-pk')
            order_quantity = request.POST.get('purchase-order-quantity')
            vendor_inventory = SellsPart.objects.filter(p_FK=raw_material_pk).first()
            vendor_inventory.p_quantity = vendor_inventory.p_quantity - int(order_quantity)
            vendor_inventory.save()

            messages.success(request, 'Raw material ordered successfully.')
            return redirect('inventory')
        else:
            messages.error(request, f'Problem ordering raw material.')
            return redirect('inventory')
    else:
        return redirect('inventory')

"""
    View that processes the creation of a raw material and redirects back to the inventory

    Information about the new raw material is accessed through the POST request and is translated into a form so that it can
    be easily validated.

    The view does a check before validation the information. If a exisiting raw material was selected, an update is made
    in the database of that raw material instead of creating a new one. If no raw material selected, the form will try validating
    the information given. If successful, the raw material will be created. Once created, the relationship between the raw material
    and the vendor selling it will be created using the CreateNewVendorOfPartForm
"""
@login_required(login_url='login')
def createRawMaterial(request):
# this view takes care of creating raw materials so that they can be selected when creating order or material 
# lists and manufacturing products
    if request.method == 'POST':
        new_rm_name = request.POST.get('new-raw-mat-name')
        if not new_rm_name == "":
            # check if name is not empty. If not empty, create new raw material (rm)
            rm_form = CreateRawMaterialForm(data={
                'p_name': new_rm_name,
                'p_unit_value': request.POST.get('new-mat-cost'),
                'p_type': 'Raw Material'
            })
            # validate the form for unique material name
            if rm_form.is_valid():
                # material does not exist yet, save the new raw material in database
                new_part = rm_form.save()
                messages.success(request, 'Raw material created.')
                return redirect('inventory')

                # create new vendor relationship for this raw material
                # v_form = CreateNewVendorOfPartForm(data={
                #     'p_FK': new_part.pk,
                #     'v_FK': request.POST.get('new-mat-vendor')
                # })
                # if v_form.is_valid():
                #     # everything is created, return with a success message
                #     v_form.save()
                    
                #     return redirect('inventory')
                # else:
                #     # return to inventory with error message
                #     messages.error(request, 'Problem finding vendor to sell raw material.')
                    
            else:
                # return to inventory with error message
                messages.error(request, 'This raw material already exists.')
                return redirect('inventory')
        else:
            if int(request.POST.get('existing-raw-mat')) == 0:
                messages.error(request, 'No raw material selected, or no name was given.')
                return redirect('inventory')
            else:
                # exisiting raw material selected, edit the raw material in database

                # fetch existing raw material, edit and save
                # TODO: add validation at this step (sprint 4)
                rm = Part.objects.get(pk=request.POST.get('existing-raw-mat'))
                rm.p_unit_value = request.POST.get('new-mat-cost')
                rm.save()

                # TODO: modify the vendor, raw material relationship (sprint 4)
                messages.info(request, 'The raw material was modified.')
                return redirect('inventory')
    else:
        return redirect('inventory')

"""
    This view is a simple URL endpoint used with ajax calls in the frontend. It's purpose is to
    validate if the passed raw material name is unique in the database by returning the raw material
    if it exists. The check is performed in the frontend.

    If an object is returned, name is not unique, else name is unique
"""
@login_required(login_url='login')
def checkUniqueRawMatName(request):
    rm_name = request.GET.get('rm_name')
    rm = Part.objects.filter(p_name=rm_name).first()
    if rm:
        json = {
            'rm_pk':rm.pk
        }
    else:
        json = {}
    return JsonResponse(json)

"""
    This view is for generating this list of specific parts and their serial number after
    a part template has been clicked on in the broader inventory.

    This view also lets users mark parts or products defective or not. (quality assurance). This
    view is triggered by an ajax call.
"""
@login_required(login_url='login')
def inventoryPartView(request):
    # get information passed in the GET request
    warehouse_id = request.GET.get('warehouse_id')
    part_id = request.GET.get('part_id')

    # get the part template that was clicked on and the warehouse
    part = Part.objects.get(pk=part_id)
    warehouse = Warehouse.objects.get(pk=warehouse_id)

    # filter the inventory for every part having the part template and inside the inventory of the warehouse clicked.
    # a part is marked as in the inventory if its attribute "p_in_inventory" = true
    inventory_parts = Contain.objects.filter(w_FK=warehouse, p_FK=part, p_in_inventory=True).all()
    context = {
        'part_name': part.p_name,
        'warehouse_name': warehouse.w_name,
        'inventory': inventory_parts,
    }
    return render(request, 'inventory-parts.html', context)

"""
    URL endpoint for toggling the defective status of a part.

    Get part from the request, toggle the p_defective attribute and return any json response for
    a success call in the ajax function
"""
@login_required(login_url='login')
def toggleInventoryPartStatus(request):
    p_serial = request.GET.get('p_serial')
    part = Contain.objects.filter(p_serial=p_serial).first()
    part.p_defective = not part.p_defective
    part.save()
    test = "success"
    return JsonResponse(test, safe=False)

"""
    URL endpoint for deleting a part from the inventory.

    **Note this action completeley deletes the record instead of setting the p_in_inventory status to false.
"""
@login_required(login_url='login')
def deleteInventoryPart(request):
    p_serial = request.GET.get('p_serial')
    part = Contain.objects.filter(p_serial=p_serial).first()
    part.delete()
    test = "success"
    messages.success(request, f"Part [{p_serial}] successfully deleted.")
    return JsonResponse(test, safe=False)

"""
    Simple URL endpoint for returning raw material. Used in an ajax call in the front end
"""
@login_required(login_url='login')
def returnRawMaterial(request):
    rm_id = request.GET.get('rm_id')
    raw_material = Part.objects.filter(pk=rm_id).all()
    rm_json = serializers.serialize('json', raw_material)
    return HttpResponse(rm_json)

"""
    Simple URL endpoint for returning vendor. Used in an ajax call in the front end
"""
@login_required(login_url='login')
def returnVendor(request):
    v_id = request.GET.get('v_id')
    vendor = Vendor.objects.filter(pk=v_id).all()
    v_json = serializers.serialize('json', vendor)
    return HttpResponse(v_json)

"""
    Simple URL endpoint for returning all selling vendors. Used in an ajax call in the front end
"""
@login_required(login_url='login')
def returnSellingVendor(request):
    rm_id = request.GET.get('rm_id')
    listOfVendors = SellsPart.objects.select_related().filter(p_FK=rm_id).all()
    vendorObjectList = []
    for vendor in listOfVendors:
        vendorObject = Vendor.objects.get(pk=vendor.v_FK.pk)
        vendorObjectList.append(vendorObject)
    rm_json = serializers.serialize('json', vendorObjectList)
    return HttpResponse(rm_json) 

"""
    Simple URL endpoint for returning all vendors. Used in an ajax call in the front end
"""
@login_required(login_url='login')
def returnAllVendor(request):
    all_vendors = Vendor.objects.all()
    all_json = serializers.serialize('json', all_vendors)
    return HttpResponse(all_json)

#This view is responsible for exporting reports on the inventory history
@login_required(login_url='login')
def download_inventory_history(request):
    items = Order.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order-history.csv"'
    writer = csv.writer(response, delimiter=',')
    #writing attributes
    writer.writerow(['Date', 'Raw Material', 'Quantity', 'Warehouse', 'Vendor', 'Cost($)', 'Status'])
    #writing data corresponding to attributes
    for obj in items:
        writer.writerow([obj.timestamp, obj.p_FK, obj.order_quantity,  obj.w_FK, obj.v_FK, obj.order_total_cost,
                         obj.order_status])
    return response
