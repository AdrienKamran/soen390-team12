from django.shortcuts import render
from .models import *
# Create your views here.
from django.shortcuts import render, redirect 
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import *

#from .filters import OrderFilter

import logging

import json

from django.http import JsonResponse

#@login_required(login_url='login')
def produceMaterialList(request):
    if request.method == 'GET':
        new_rm_name = request.GET.get('product')
        new_wh_name = request.GET.get('warehouse')
        mulQty = int(request.GET.get('qty'))
        #new_rm_name = 'Product Test 4'
        #new_wh_name = 'Test Warehouse'
        #mulQty = 1
        runTotal = 0
        resp = {'0':1, '1':1.05}
        if not new_rm_name == "":
            # create a new raw material
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                matList = MadeOf.objects.filter(part_FK_parent=existing_rm).all()
                if matList:
                    existing_wh = Warehouse.objects.filter(w_name=new_wh_name).first()
                    if existing_wh:
                        counter = 2
                        qty=0
                        prx=0
                        tot =0
                        sto=0
                        nom=""
                        for p in matList:
                            qty = p.quantity
                            prx = p.part_FK_child.p_unit_value
                            nom = p.part_FK_child.p_name
                            tot = qty*prx
                            existing_wh_entry = Contains.objects.filter(w_FK=existing_wh,p_FK=p.part_FK_child).first()
                            if existing_wh_entry:
                                sto = existing_wh_entry.p_quantity
                                resp [counter] = {
                                    "name":nom,
                                    "price":prx,
                                    "quantity":qty,
                                    "total":tot,
                                    "store":sto
                                }
                                counter=counter+1
                                runTotal = runTotal +tot
                            else:
                                messages.error(request, 'warehouse does not have items.')
                        resp['0'] = resp['0']*float(runTotal)*mulQty
                        resp['1'] = resp['1']*float(runTotal)*mulQty
        return JsonResponse(resp)


#@login_required(login_url='login')
def createMaterialList(request):
    if request.method == 'POST':
        parent_part = None
        new_rm_name = request.POST.get('product-name')
        is_bike = request.POST.get('bicycle-check')
        if not new_rm_name == "":
            # create a new raw material
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                messages.error(request, 'This material list already exists.')
                return redirect('manufacturing')
            else:
                # material doesn't exist yet
                new_rm = Part(p_name=new_rm_name, p_type='Part', p_unit_value=0)
                if is_bike:
                    new_rm.p_type='Product'
                    new_rm.save()
                else:
                    new_rm.save()
                parent_part = new_rm
        bike = False
        parts = {}
        counter = 0
        for key in request.POST:
            if key == "product-name":
                continue
            if key == "bicycle-check":
                continue
            if "component" in key:
                #skip this line if its the quantity we look this up later
                if "component-qty" in key:
                    continue
                #this is a generated component
                value = request.POST[key]
                counter = int(request.POST[key+"-qty"])
                 # create a new raw material
                existing_rm = Part.objects.filter(p_name=value).first()
                if existing_rm:
                    new_rel = MadeOf(part_FK_parent=parent_part, part_FK_child = existing_rm, quantity=counter)
                    new_rel.save()
                    #update price
                    parent_part.p_unit_value = parent_part.p_unit_value+(existing_rm.p_unit_value * new_rel.quantity)
                    parent_part.save()
    return redirect('manufacturing')         

#@login_required(login_url='login')
def manufacturingViewPage(request):
    #define everything as None to start to cover relation not found errors
    parts = Part.objects.all()
    warehouses = Warehouse.objects.all()
    made = MadeOf.objects.all()
    contain = Contains.objects.all()
    #Call all the itmes that we need to render these templates
    data = {
        'parts':parts,
        'warehouse':warehouses,
        'made':made,
        'contain':contain,
    }
    return render(request, template_name='manufacturing.html', context=data)

@login_required(login_url='login')
def manufactureProduct(request):
    if request.method == 'POST':
        part_name = request.POST.get('choose-material-list')
        warehouse_name = request.POST.get('warehouse-destination')
        quantity = int(request.POST.get('produce-quantity'))

        part = Part.objects.filter(p_name=part_name).first()
        warehouse = Warehouse.objects.filter(w_name=warehouse_name).first()
        # get all the raw material is the part is made of

        sub_parts = MadeOf.objects.filter(part_FK_parent=part.pk).all()
        for sub_part in sub_parts:
            # remove the quantity from the warehouse
            w_inventory = Contains.objects.filter(p_FK=sub_part.part_FK_child.pk, w_FK=warehouse.pk).first()
            w_inventory.p_quantity = w_inventory.p_quantity - (sub_part.quantity * quantity)
            w_inventory.save()

        #check if new part already exists in warehouse
        existing_part = Contains.objects.filter(p_FK=part, w_FK=warehouse).first()
        if existing_part:
            #modify quantity
            existing_part.p_quantity = existing_part.p_quantity + quantity
            existing_part.save()
        else:
            new_part = Contains(p_FK=part, w_FK=warehouse, p_quantity=quantity)
            new_part.save()

        messages.success(request, "Part successfully manufactured and placed in the warehouse.")
        return redirect('inventory')
    else:
        return redirect('manufacturing')