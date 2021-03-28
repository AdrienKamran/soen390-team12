from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from dashboard.decorators import *

# Create your views here.

@login_required(login_url='login')
def vendors(request):
    return render(request, template_name='vendors.html', context={})

