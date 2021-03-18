from django.shortcuts import render, redirect 
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from inventory.models import *
from accounting.models import *
from manufacturing.models import *

from decimal import Decimal

import logging
import json

"""
"""
@login_required(login_url='login')
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
                            existing_part_count = len(Contain.objects.filter(w_FK=existing_wh, p_FK=p.part_FK_child, p_defective=False, p_in_inventory=True).all())
                            sto = existing_part_count
                                
                            resp [counter] = {
                                "name":nom,
                                "price":prx,
                                "quantity":qty*mulQty,
                                "total":tot,
                                "store":sto
                            }
                            counter=counter+1
                            runTotal = runTotal +tot
                        resp['0'] = resp['0']*float(runTotal)*mulQty
                        resp['1'] = resp['1']*float(runTotal)*mulQty
        return JsonResponse(resp)

"""
"""
@login_required(login_url='login')
def loadMaterialList(request):
    if request.method == 'GET':
        new_rm_name = request.GET.get('product')
        resp = {'0':False}
        if not new_rm_name == "":
            # find the part and get a material list for said part
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                matList = MadeOf.objects.filter(part_FK_parent=existing_rm).all()
                if existing_rm.p_type=='Product':
                    resp['0']=True
                if matList:
                    #existing_wh = Warehouse.objects.filter(w_name=new_wh_name).first()
                    #if existing_wh:
                    counter = 1
                    qty=0
                    nom=""
                    for p in matList:
                        qty = int(p.quantity)
                        nom = p.part_FK_child.p_name
                        resp [counter] = {
                            "name":nom,
                            "quantity":qty,
                        }
                        counter=counter+1        
        return JsonResponse(resp)

"""
"""
@login_required(login_url='login')
def createMaterialList(request):
    if request.method == 'POST':
        parent_part = None
        new_rm_name = request.POST.get('product-name')
        is_bike = request.POST.get('bicycle-check')
        if not new_rm_name == "":
            # create a new raw material
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                messages.error(request, 'This material list already exists... Updating Material List')
                #Find and delete the old mat list then set parent part to the exisitng part
                old_mat_list = MadeOf.objects.filter(part_FK_parent=existing_rm).all()
                old_mat_list.delete()
                parent_part = existing_rm
                #return redirect('manufacturing')
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

"""
"""
@login_required(login_url='login')
def manufacturingViewPage(request):
    #define everything as None to start to cover relation not found errors
    parts = Part.objects.all()
    warehouses = Warehouse.objects.all()
    made = MadeOf.objects.all()
    contain = Contain.objects.all()
    #Call all the itmes that we need to render these templates
    data = {
        'parts':parts,
        'warehouse':warehouses,
        'made':made,
        'contain':contain,
    }
    return render(request, template_name='manufacturing.html', context=data)

"""
    URL endpoint that handles the creation/manufacturing of a product.

    It first gets the information passed by the POST request, and queries the database for the part template and the warehouse
    source/destination. It also queries the MadeOf table to get all the sub parts required for manufacturing the part.

    It then validates that every sub part is in enough quantity in the source warehouse to manufacture the product. If one or more sub-parts
    are missing in the inventory, endpoint returns error message.

    Next step is to "remove" the used sub-parts in the inventory by setting the property p_in_inventory to false
    (for history purposes, we want to keep track of every part that has existed in the inventory)
    When all the sub-parts have been removed, the product is created inside the inventory

    It then creates a Manufacture order and a transaction to match this order in the accounting tab. The last step is to link all the manufactured
    products to the manufacture order for tracking purposes.
"""
@login_required(login_url='login')
def manufactureProduct(request):
    if request.method == 'POST':
        part_name = request.POST.get('choose-material-list')
        warehouse_name = request.POST.get('warehouse-destination')
        quantity = int(request.POST.get('produce-quantity'))
        price = float(request.POST.get('final-price'))

        part = Part.objects.filter(p_name=part_name).first()
        warehouse = Warehouse.objects.filter(w_name=warehouse_name).first()
        # get all the raw material is the part is made of

        sub_parts = MadeOf.objects.select_related().filter(part_FK_parent=part.pk).all()

        # first, query the warehouse for every sub-part and make sure they are available
        for sub_part in sub_parts:
            sub_part_count = len(Contain.objects.filter(w_FK=warehouse.pk, p_FK=sub_part.part_FK_child.pk, p_defective=False, p_in_inventory=True).all())
            if sub_part_count < sub_part.quantity * quantity:
                messages.error(request, f"Insufficient parts. Missing {(sub_part.quantity * quantity) - sub_part_count} unit(s) of the part: {sub_part.part_FK_child.p_name}.")
                return redirect('manufacturing')

        # if we reach the end of the for loop, this means we have enough quantity of every part(s).
        # second step is to remove the parts needed to manufacture the product from the warehouse

        for sub_part in sub_parts:
            i = 0
            while i < sub_part.quantity * quantity:
                part_in_stock = Contain.objects.filter(w_FK=warehouse.pk, p_FK=sub_part.part_FK_child.pk, p_defective=False, p_in_inventory=True).first()
                part_in_stock.p_in_inventory = False
                part_in_stock.save()
                i = i + 1

        # every sub part is now removed from inventory
        # last step is to add the amount of new products into the inventory

        # get the serial number of the last added part/product/raw material
        last_index_object = Contain.objects.order_by('-p_serial').first()
        last_index = 0
        if last_index_object is None:
            last_index = 10000
        else:
            last_index = last_index_object.p_serial

        # create manufacture history record
        new_manufacture = Manufacture(p_FK=part, w_FK=warehouse, manufacture_quantity=quantity, manufacture_total_cost=price)
        new_manufacture.save()

        t_last_index_object = Transaction.objects.order_by('-t_serial').first()
        t_last_index = 0
        if t_last_index_object is None:
            t_last_index = 500000
        else:
            t_last_index = t_last_index_object.t_serial + 1

        # create transaction
        new_transaction = Transaction(t_type='MANUFACTURE', t_balance=-price, t_item_name=part.p_name, t_serial=t_last_index, t_quantity=quantity)
        new_transaction.save()
        

        i = 0
        while i < quantity:
            last_index = last_index + 1
            new_part = Contain(p_FK=part, w_FK=warehouse, p_serial=last_index, p_defective=False, p_in_inventory=True)
            new_part.save()
            new_manufacture_part = ManufacturesPart(m_FK=new_manufacture, c_FK=new_part)
            new_manufacture_part.save()

            if part.p_type == 'Product':
                # This part is a product therefore we need to create a record in the product table
                # For now, this product information is entered by default
                product_price = Decimal(1.2) * part.p_unit_value
                new_product = Product(c_FK=new_part, selling_price=product_price, prod_type='Mountain Bike', prod_weight=Decimal(70.59))
                new_product.save()

            i = i + 1

        # every object should now be created and added to the inventory with their unique serial number

        messages.success(request, "Part successfully manufactured and placed in the warehouse.")
        return redirect('inventory')
    else:
        return redirect('manufacturing')
