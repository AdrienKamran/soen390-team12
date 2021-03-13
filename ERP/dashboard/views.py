from django.shortcuts import render, redirect 
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from inventory.models import *
from .forms import CreateUserForm, OrderRawMaterialForm, CreateRawMaterialForm, CreateNewVendorOfPartForm
#from .filters import OrderFilter
from datetime import datetime
from decimal import Decimal
import logging

import io
import csv
import json


from reportlab.pdfgen import canvas

#from reportlab.pdfgen import canvas

# Create logger
logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, "landing.html")

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():           
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            logger.debug("creating account with name: " + user)
            return redirect('login')             
    context = {'form': form}
    return render(request, 'register.html', context)



@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.debug(username + " has logged in")
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            logger.debug(username + " entered incorrect password")
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    logger.debug("User has logged out")
    return redirect('login')

@login_required(login_url='login')
def inventory(request):
    context = {}
    if request.method == 'POST':
        var = 0
    else:
        # filters for distinct values of the tuple warehouse and part.
        # eg. A part template will show only once for the same warehouse, but more than once
        # if in different warehouses.
        part_inventory = Contains.objects.select_related().distinct('p_FK', 'w_FK')
        raw_material_all = Part.objects.filter(p_type='Raw Material').all()
        warehouse_all = Warehouse.objects.all()
        vendor_all = Vendor.objects.all()
        orders = Orders.objects.select_related().all().order_by('timestamp')
        date_of_day = datetime.now()

        # figure out how to show the count for every object.
        part_inventory_count = {}
        for part in part_inventory:
            part_inventory_count[part.p_serial] = len(Contains.objects.filter(p_FK=part.p_FK, w_FK=part.w_FK).all())
        context = {
            'inventory': part_inventory,
            'inventory_count': part_inventory_count,
            'raw_material_all': raw_material_all,
            'warehouse_all': warehouse_all,
            'vendor_all': vendor_all,
            'rm_orders': orders,
            'date_of_day': date_of_day
        }
    return render(request, 'inventory.html', context=context)

#decided to combine the two endpoints together
def generateReport(request):
    if request.method =='GET':
        queryDict = request.GET
        reportFormat = queryDict.get('format', None)
        if reportFormat == 'CSV':
            return generateCSV(request)
        if reportFormat == 'PDF':
            return generatePDF(request)
        else:
            return HttpResponseNotFound("No report in supplied format")
    else:
        return HttpResponseNotFound("Could not process your request") 


def generatePDF(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    #register valid get requests
    p=None
    report =None
    if request.method == 'GET':
        queryDict = request.GET
        report = queryDict.get('report', None)
        if report=='TEST':
            p = drawTestReport(buffer)
        else:
            return HttpResponseNotFound("There is no valid report")
    else:
        return HttpResponseNotFound("Could not process your request")
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=report+'.pdf')

"""
#   Setup the different PDF templates here (draw+reportName)
"""

def drawTestReport(buffer):
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    return p



def generateCSV(request):
    response = None
    report =None
    if request.method == 'GET':
        queryDict = request.GET
        report = queryDict.get('report', None)
        if report=='TEST':
            response = writeTestReport()
        else:
            return HttpResponseNotFound("There is no valid report")
    else:
        return HttpResponseNotFound("Could not process your request")
    return response

"""
#   Setup the different CSV tamplates here (write+reportName)
"""

def writeTestReport():
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="test.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response

@login_required(login_url='login')
def salesViewPage(request):
    return render(request, template_name='sales.html', context={})

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
'''
@login_required(login_url='login')
def returnVendorOfPart(request):
    p_id = request.GET.get('p_id')
    vendors = SellsParts.objects.select_related().filter(p_FK=2).all()
    v_list = []
    for vendor in vendors:
        v_list.append({'v_fk':vendor.v_FK, 'v_name':vendor.v_FK.v_name})
    return json.dumps(v_list)
'''
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

            #first, check if there is existing raw material in the warehouse inventory
            rm = Contains.objects.filter(p_FK=new_order.p_FK.pk, w_FK=new_order.w_FK.pk).first()
            if rm:
                #this material already exists
                rm.p_quantity = rm.p_quantity + new_order.order_quantity
                rm.save()
            else:
                new_rm = Contains(p_FK=new_order.p_FK, w_FK=new_order.w_FK, p_quantity=new_order.order_quantity)
                new_rm.save()

            messages.success(request, 'Raw material ordered successfully.')
            return redirect('inventory')
        else:
            messages.error(request, f'Problem ordering raw material.')
            return redirect('inventory')
    else:
        return redirect('inventory')

@login_required(login_url='login')
def createRawMaterial(request):
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
                    'v_FK':request.POST.get('new-mat-vendor')
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
