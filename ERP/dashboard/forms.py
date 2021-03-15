from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from inventory.models import Orders, Part, SellsParts
from sales.models import Customer


class CreateUserForm(UserCreationForm):
    class Meta:        
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrderRawMaterialForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['v_FK', 'p_FK', 'w_FK', 'order_quantity', 'order_total_cost']

class CreateRawMaterialForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['p_name', 'p_unit_value', 'p_type']

class CreateNewVendorOfPartForm(forms.ModelForm):
    class Meta:
        model = SellsParts
        fields = ['p_FK', 'v_FK']

class CreateNewCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'type', 'email', 'phone_number', 'address_line', 'city', 'state', 'zip_code', 'country']
