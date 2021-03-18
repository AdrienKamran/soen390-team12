from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from inventory.models import Order, Part, SellsPart

"""
    For for creating a new user using the model User
"""
class CreateUserForm(UserCreationForm):
    class Meta:        
        model = User
        fields = ['username', 'email', 'password1', 'password2']

"""
    For for ordering raw material
"""
class OrderRawMaterialForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['v_FK', 'p_FK', 'w_FK', 'order_quantity', 'order_total_cost']

"""
    Form for creating a new raw material
"""
class CreateRawMaterialForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['p_name', 'p_unit_value', 'p_type']

"""
    Form for creating a new vendor selling a certain part
"""
class CreateNewVendorOfPartForm(forms.ModelForm):
    class Meta:
        model = SellsPart
        fields = ['p_FK', 'v_FK']