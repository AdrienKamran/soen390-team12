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
        new_rm_name = request.POST.get('product')
        new_wh_name = request.POST.get('warehouse')
        mulQty = int(request.POST.get('qty'))
        runTotal = 0
        resp = {'0':1, '1':1.05}
        if not new_rm_name == "":
            # create a new raw material
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                matList = MadeOf.objects.filter(part_FK_parent=existing_rm).all()
                if existing_wh:
                    # return to inventory with error message
                    messages.success(request, 'Found Part.')
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
                            existing_wh_entry = Containsresp['0'] = resp['0']*runTotal.objects.filter(w_FK=existing_wh,p_FK=existing_rm).first()
                            if existing_wh_entry:
                                sto = existing_wh_entry.p_quantity
                                resp[''+counter] = {
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
                        resp['0'] = resp['0']*runTotal
                        resp['1'] = resp['1']*runTotal
                else:
                    # material doesn't exist yet
                    messages.error(request, 'Could not find list.')
            else:
                messages.error(request, 'Could not find part.')
        return JsonResponse(resp)


#@login_required(login_url='login')
def createMaterialList(request):
    if request.method == 'POST':
        parent_part = None
        new_rm_name = request.POST.get('product-name')
        if not new_rm_name == "":
            # create a new raw material
            existing_rm = Part.objects.filter(p_name=new_rm_name).first()
            if existing_rm:
                parent_part = existing_rm
                # return to inventory with error message
                messages.success(request, 'This part already exists.')
            else:
                # material doesn't exist yet
                new_rm = Part(p_name=new_rm_name)
                new_rm.save()
                parent_part = new_rm
                messages.success(request, 'Raw material created.')
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
                existing_rm = Part.objects.filter(rm_name=value).first()
                if existing_rm:
                    # return to inventory with error message
                    new_rel = MadeOf(part_FK_parent=parent_part, part_FK_child = existing_rm, quantity=counter)
                    new_rel.save()
                    messages.success(request, 'Part relation added.')
                else:
                    # material doesn't exist yet
                    messages.error(request, 'Part not found.')
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
