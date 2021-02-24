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





#@login_required(login_url='login')
def createMaterialList(request):
    if request.method == 'POST':
        productName = None
        bike = False
        parts = {}
        counter = 0
        for key in request.POST:
            if key == "product-name":
                productName = request.POST[key]
            if key == "bicycle-check":
                bike = True
            if "component" in key:
                #this is a generated component
                value = request.POST[key]
                parts[counter] = value
                counter = counter+1
    return redirect('manufacturing')             



@login_required(login_url='login')
def salesViewPage(request):
    return render(request, template_name='sales.html', context={})


#@login_required(login_url='login')
def manufacturingViewPage(request):
    #define everything as None to start to cover relation not found errors
    products = None
    materials = None
    warehouses = None
    madeR = None
    madeP = None
    containR = None
    containP = None
    #Call all the itmes that we need to render these templates
    try:
        products = Part.objects.all()
        print(products)
    except:
        pass
    try:
        materials = Part.objects.all()
        print(materials)
    except:
        pass
    try:
        warehouses = Warehouse.objects.all()
        print(warehouses)
    except:
        pass
    try:
        madeR = MadeOf.objects.all()
        print(madeR)
    except:
        pass
    try:
        madeP = MadeOf.objects.all()
        print(madeP)
    except:
        pass
    try:
        containR = Contains.objects.all()
        print(containR)
    except:
        pass
    try:
        containP = Contains.objects.all()
        print(containP)
    except:
        pass
    data = {
        'products':products,
        'materials':materials,
        'warehouse':warehouses,
        'madeR':madeR,
        'madeP':madeP,
        'containR':containR,
        'containP':containP,
        'productionRequest':"[{'name': 'Steel','qty': 15,'avi': 7},{'name': 'Leather','qty': 5,'avi': 8}]",
        'productionRequestValue':1,
        'productionRequestValueMul':1.5
    }

    return render(request, template_name='manufacturing.html', context=data)
