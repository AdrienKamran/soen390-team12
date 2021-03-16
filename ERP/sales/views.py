from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import OrderForm, CustomerForm
from .models import *

@login_required(login_url='login')
def sales_view(request, order_form=None, customer_form=None):
    tab = 'sell-tab'
    if order_form is None:
        order_form = OrderForm()
    if customer_form is None:
        customer_form = CustomerForm()
    else:
        tab = 'customer-tab'
    order_history = SalesOrder.objects.all().order_by('-date_created')
    return render(request, 'sales.html', {'order_form' : order_form, 'customer_form' : customer_form, 'order_history' : order_history, 'tab' : tab})

@login_required(login_url='login')
def add_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            name = customer_form.cleaned_data['name']
            customer_type = customer_form.cleaned_data['type']
            email = customer_form.cleaned_data['email']
            phone_number = customer_form.cleaned_data['phone_number']
            address_line = customer_form.cleaned_data['address_line']
            city = customer_form.cleaned_data['city']
            state = customer_form.cleaned_data['state']
            zip_code = customer_form.cleaned_data['zip_code']
            country = customer_form.cleaned_data['country']
            if not Customer.objects.filter(name=name, address_line=address_line).exists():
                customer = Customer(
                    name=name,
                    type=customer_type,
                    email=email,
                    phone_number=phone_number,
                    address_line=address_line,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    country=country
                )
                customer.save()
                return HttpResponseRedirect('/sales')
            else:
                customer_form.add_error('name',"Customer already exists.")
        return sales_view(request, customer_form=customer_form)
    return HttpResponseRedirect('/sales')

@login_required(login_url='login')
def add_sale_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            customer = order_form.cleaned_data['customer']
            product = order_form.cleaned_data['product']
            warehouse = order_form.cleaned_data['warehouse']
            if customer and product:
                delivery_date = order_form.cleaned_data['delivery_date']
                quantity = order_form.cleaned_data['quantity']
                status = order_form.cleaned_data['status']
                sale_total = quantity * product.selling_price
                order = SalesOrder(
                    customer=customer,
                    delivery_date=delivery_date,
                    product=product,
                    quantity=quantity,
                    warehouse=warehouse,
                    sale_total=sale_total,
                    status=status
                )
                order.save()
                return HttpResponseRedirect('/sales')
            else:
                order_form.add_error(None, "Customer or product is invalid")
        return render(request, 'sales.html', {'order_form' : order_form, 'tab' : 'sell-tab'})