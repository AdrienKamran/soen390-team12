from django.forms import ModelForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from inventory.models import Orders


class CreateUserForm(UserCreationForm):
    class Meta:        
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrderRawMaterialForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['v_FK', 'p_FK', 'w_FK', 'order_quantity', 'order_total_cost']