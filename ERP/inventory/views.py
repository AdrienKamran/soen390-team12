from django.shortcuts import render, redirect 
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
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


@login_required(login_url='login')
def inventory(request):
    # this takes care of generating all the information for the inventory view.
    context = {}
    if request.method == 'POST':
        var = 0
    else:
        # filters for distinct values of the tuple warehouse and part.
        # eg. A part template will show only once for the same warehouse, but more than once
        # if in different warehouses.
        part_inventory = Contain.objects.select_related().filter(p_in_inventory=True).distinct('p_FK', 'w_FK') # inventory of the different part types in each warehouse
        raw_material_all = Part.objects.filter(p_type='Raw Material').all() # list of all the raw materials in the parts list
        warehouse_all = Warehouse.objects.all() # list of all the warehouses
        vendor_all = Vendor.objects.all() # list of all the vendors
        orders = Order.objects.select_related().all().order_by('timestamp') # list of all the orders
        date_of_day = datetime.now() # today's datetime

        # for every part in the list, find how many of those parts exist in the warehouse and save in a dictionary to be
        # accessible in the inventoy template
        part_inventory_count = {}
        for part in part_inventory:
            part_inventory_count[part.p_serial] = len(Contain.objects.filter(p_FK=part.p_FK, w_FK=part.w_FK, p_in_inventory=True).all())
        context = {
            'inventory': part_inventory,
            'inventory_count': part_inventory_count,
            'raw_material_all': raw_material_all,
            'warehouse_all': warehouse_all,
            'vendor_all': vendor_all,
            'rm_orders': orders,
            'date_of_day': date_of_day
        }
    return render(request, 'inventory.html', context=context) # render the view


@login_required(login_url='login')
def orderRawMaterial(request):
    if request.method == 'POST':
        # Use form to validate information automatically
        cost = Decimal(request.POST.get('total-cost'))
        cost_rounded = round(cost, 2)
        form = OrderRawMaterialForm(data={
            'v_FK': request.POST.get('purchase-vendor-pk'),
            'w_FK': request.POST.get('warehouse-pk'),
            'p_FK': request.POST.get('raw-mat-pk'),
            'order_quantity': request.POST.get('purchase-order-quantity'),
            'order_total_cost': cost_rounded
        })
        if form.is_valid():
            # save the new record
            new_order = form.save()
            new_order.order_status = 'RECEIVED'
            new_order.save()
            # for the sake of this sprint, the order is automatically shipped and appears in the warehouse inventory

            t_last_index_object = Transaction.objects.order_by('-t_serial').first()
            t_last_index = 0
            if t_last_index_object is None:
                t_last_index = 500000
            else:
                t_last_index = t_last_index_object.t_serial + 1

            # create transaction
            new_transaction = Transaction(t_type='ORDER', t_balance=-cost_rounded, t_item_name=new_order.p_FK.p_name, t_serial=t_last_index, t_quantity=new_order.order_quantity)
            new_transaction.save()
        

            # before adding the new parts, query the contains list for the last index.
            last_index_object = Contain.objects.order_by('-p_serial').first()
            last_index = 0
            if last_index_object is None:
                last_index = 10000
            else:
                last_index = last_index_object.p_serial
            i = 0

            while i < int(request.POST.get('purchase-order-quantity')):
                last_index = last_index + 1
                new_rm = Contain(p_FK=new_order.p_FK, w_FK=new_order.w_FK, p_serial=last_index, p_defective=False, p_in_inventory=True)
                new_rm.save()

                new_order_part = OrdersPart(o_FK=new_order, c_FK=new_rm)
                new_order_part.save()
                i = i + 1

            messages.success(request, 'Raw material ordered successfully.')
            return redirect('inventory')
        else:
            messages.error(request, f'Problem ordering raw material.')
            return redirect('inventory')
    else:
        return redirect('inventory')


@login_required(login_url='login')
def createRawMaterial(request):
# this view takes care of creating raw materials so that they can be selected when creating order or material 
# lists and manufacturing products
    if request.method == 'POST':
        new_rm_name = request.POST.get('new-raw-mat-name')
        if not new_rm_name == "":
            # create a new raw material
            rm_form = CreateRawMaterialForm(data={
                'p_name': new_rm_name,
                'p_unit_value': request.POST.get('new-mat-cost'),
                'p_type': 'Raw Material'
            })
            if rm_form.is_valid():
                # material does not exist yet
                new_part = rm_form.save()

                v_form = CreateNewVendorOfPartForm(data={
                    'p_FK': new_part.pk,
                    'v_FK': request.POST.get('new-mat-vendor')
                })
                if v_form.is_valid():
                    v_form.save()
                    messages.success(request, 'Raw material created.')
                    return redirect('inventory')
                else:
                    # return to inventory with error message
                    messages.error(request, 'Problem finding vendor to sell raw material.')
                    return redirect('inventory')
            else:
                # return to inventory with error message
                messages.error(request, 'This raw material already exists.')
                return redirect('inventory')
        else:
            # edit existing raw material

            #add validation
            rm = Part.objects.get(pk=request.POST.get('existing-raw-mat'))
            rm.p_unit_value = request.POST.get('new-mat-cost')
            rm.save()

            # edit who sells the raw material
            messages.info(request, 'The raw material was modified.')
            return redirect('inventory')
    else:
        return redirect('inventory')


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


@login_required(login_url='login')
def inventoryPartView(request):
    warehouse_id = request.GET.get('warehouse_id')
    part_id = request.GET.get('part_id')

    part = Part.objects.get(pk=part_id)
    warehouse = Warehouse.objects.get(pk=warehouse_id)
    inventory_parts = Contain.objects.filter(w_FK=warehouse, p_FK=part, p_in_inventory=True).all()

    context = {
        'part_name': part.p_name,
        'warehouse_name': warehouse.w_name,
        'inventory': inventory_parts,
    }
    return render(request, 'inventory-parts.html', context)


@login_required(login_url='login')
def toggleInventoryPartStatus(request):
    p_serial = request.GET.get('p_serial')

    part = Contain.objects.filter(p_serial=p_serial).first()
    part.p_defective = not part.p_defective
    part.save()

    test = "success"
    return JsonResponse(test, safe=False)


@login_required(login_url='login')
def deleteInventoryPart(request):
    p_serial = request.GET.get('p_serial')

    part = Contain.objects.filter(p_serial=p_serial).first()
    part.delete()

    test = "success"
    messages.success(request, f"Part [{p_serial}] successfully deleted.")
    return JsonResponse(test, safe=False)


@login_required(login_url='login')
def returnRawMaterial(request):
    rm_id = request.GET.get('rm_id')
    raw_material = Part.objects.filter(pk=rm_id).all()
    rm_json = serializers.serialize('json', raw_material)
    return HttpResponse(rm_json)


@login_required(login_url='login')
def returnVendor(request):
    v_id = request.GET.get('v_id')
    vendor = Vendor.objects.filter(pk=v_id).all()
    v_json = serializers.serialize('json', vendor)
    return HttpResponse(v_json)
