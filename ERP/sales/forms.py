from django import forms
from django.forms import ModelChoiceField

from inventory.models import *
from sales.models import *

#To render prod_type for the label for Product in OrderForm
class ProductModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.p_name

#To render w_name for label for Warehouse in OrderForm
class WarehouseModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.w_name

class OrderForm(forms.Form):
    status_choice = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )

    customer = forms.ModelChoiceField(label='Customer Name', queryset=None)
    delivery_date = forms.DateField(label='Delivery Date', widget=forms.SelectDateWidget)
    product = ProductModelChoiceField(label='Part', queryset=None)
    quantity = forms.IntegerField(label='Quantity')
    warehouse = WarehouseModelChoiceField(label='Warehouse Source', queryset=None)
    status = forms.CharField(label='Status', widget=forms.Select(choices=status_choice))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()
        self.fields['product'].queryset = Part.objects.filter(p_type='Product').all()
        self.fields['warehouse'].queryset = Warehouse.objects.all()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'type', 'email', 'phone_number', 'address_line', 'city', 'state', 'zip_code', 'country']
