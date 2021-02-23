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






@login_required(login_url='login')
def salesViewPage(request):
    return render(request, template_name='sales.html', context={})


@login_required(login_url='login')
def manufacturingViewPage(request):
    #Call all the itmes that we need to render these templates
    products = Products.objects.all()
    materials = RawMaterials.objects.all()
    warehouses = Warehouse.objects.all()
    madeR = MadeOfRM.objects.all()
    madeP = MadeOfParts.objects.all()
    containR = ContainsRM.objects.all()
    containP = ContainsProducts.objects.all()
    data = {
        'products':products,
        'materials':materials,
        'warehouse':warehouses,
        'madeR':madeR,
        'madeP':madeP,
        'containR':containR,
        'containP':containP,
        'productionRequest':"[{'name': 'Steel','qty': 15,'avi': 7},{'name': 'Leather','qty': 5,'avi': 8}]",
        'productionRequestValue':1
    }

    return render(request, template_name='manufacturing.html', context=data)
