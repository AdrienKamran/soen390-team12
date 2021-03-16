from django import forms

from inventory.models import Warehouse, Product
from sales.models import Customer


class OrderForm(forms.Form):
    customer_list = Customer.objects.all().values_list('id', 'name')
    product_list = Product.objects.all().values_list('id', 'prod_type')
    warehouse_list = Warehouse.objects.all().values_list('id', 'w_name')
    status_choice = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    customer = forms.IntegerField(label='Customer', widget=forms.Select(choices=customer_list))
    delivery_date = forms.DateField(label='Delivery Date', widget=forms.SelectDateWidget)
    product = forms.IntegerField(label='Product', widget=forms.Select(choices=product_list))
    quantity = forms.IntegerField(label='Quantity')
    warehouse = forms.IntegerField(label='Warehouse Source', widget=forms.Select(choices=warehouse_list))
    status = forms.CharField(label='Status', widget=forms.Select(choices=status_choice))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'type', 'email', 'phone_number', 'address_line', 'city', 'state', 'zip_code', 'country']
