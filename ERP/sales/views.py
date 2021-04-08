import csv, io

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponse

from sales.forms import OrderForm, CustomerForm
from sales.models import *
from inventory.models import *
from accounting.models import *
from notifications.forms import SubscriptionCreateForm
from notifications.models import Subscription

#This view displays the all the necessary information regarding the sales template.
@login_required(login_url='login')
def sales_view(request, order_form=None, customer_form=None, sales_tab=None):
    User = get_user_model()
    users = User.objects.all()
    if sales_tab is None:
        tab = 'sell-tab'
    else:
        tab = sales_tab
    if order_form is None:
        order_form = OrderForm()
    if customer_form is None:
        customer_form = CustomerForm()
    else:
        tab = 'customer-tab'

    order_history = SalesOrder.objects.order_by('-pk').all()
    customers = Customer.objects.all()

    return render(request, 'sales.html',
                  {'order_form': order_form, 'customer_form': customer_form, 'order_history': order_history,
                   'tab': tab, 'customers': customers, 'users': users})

#This view handles the post request that are made to create new customers.
#It validates if a customer already exists or not and validate the form fields
#If all the information is provided correctly, a customer is created in the database and the sales_view function is called
#to return the sales template.
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
                messages.success(request, name + ' was created successfully')
                return HttpResponseRedirect('/sales')
            else:
                customer_form.add_error('name', "Customer already exists.")
        return sales_view(request, customer_form=customer_form)
    return HttpResponseRedirect('/sales')

# This view is responsible for creating a sale order for a customer. It takes the input fields from the post request of the form
# it validates them, then it adds a recrod to SalesOrder
@login_required(login_url='login')
def add_sale_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            customer = order_form.cleaned_data['customer']
            product = order_form.cleaned_data['product']
            warehouse = order_form.cleaned_data['warehouse']
            # product is the part template chosen from the form
            # get the quantity in the warehouse
            product_quantity = len(
                Contain.objects.filter(p_FK=product, w_FK=warehouse, p_defective=False, p_in_inventory=True).all())
            if product_quantity > 0:
                # Get the selling price
                selling_price = Product.objects.filter(
                    c_FK=Contain.objects.filter(p_FK=product, w_FK=warehouse, p_defective=False,
                                                p_in_inventory=True).first()).first().selling_price
                #If the customer and product exist then we can proceed with the order details
                if customer and product:
                    delivery_date = order_form.cleaned_data['delivery_date']
                    quantity = order_form.cleaned_data['quantity']
                    status = order_form.cleaned_data['status']
                    sale_total = quantity * selling_price
                    if product_quantity >= quantity:
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
                        #Once an order has been placed, we add a record in the soldItems, so we can use it later to display
                        #stats about all of our sold items.
                        soldCount = SoldItems.objects.filter(product=product).first()
                        #If an existing product is sold, then we increment the quatity of this product based on the ordered quantity
                        if soldCount is not None:
                            soldCount.count = soldCount.count + quantity
                            soldCount.save()
                        #else we create a new record for this product and we set the quantity to the ordered quantity    
                        else:
                            new_soldCount = SoldItems(
                                product=product,
                                count=quantity
                            ) 
                            new_soldCount.save()   
                        # Create sale transaction for the accounting tab
                        t_last_index_object = Transaction.objects.order_by('-t_serial').first()
                        t_last_index = 0
                        if t_last_index_object is None:
                            t_last_index = 500000
                        else:
                            t_last_index = t_last_index_object.t_serial + 1
                        # create transaction
                        new_transaction = Transaction(t_type='SALE', t_balance=order.sale_total,
                                                      t_item_name=order.product.p_name, t_serial=t_last_index,
                                                      t_quantity=order.quantity)
                        new_transaction.save()
                        # Add the products sold to the SalePart table and remove from inventory
                        i = 0
                        while i < quantity:
                            # get the first product
                            product_sold = Contain.objects.filter(p_FK=product, w_FK=warehouse, p_defective=False,
                                                                  p_in_inventory=True).first()
                            # add record
                            new_sales_part_record = SalesPart(s_FK=order, c_FK=product_sold)
                            new_sales_part_record.save()
                            # remove from inventory
                            product_sold.p_in_inventory = False
                            product_sold.save()
                            i = i + 1
                        messages.success(request,'The sale order has been created successfully.')
                        return HttpResponseRedirect('/sales')
                    else:
                        messages.error(request,'Not enough product in inventory.')
                else:
                    messages.error(request, product.p_name + 'does not exist in this warehouse.')
            else:
                order_form.add_error(None, "Customer or product is invalid.")
        return render(request, 'sales.html', {'order_form': order_form, 'tab': 'sell-tab'})

#This view is responsible for setting status of each order in the salesOrder model
@login_required(login_url='login')
def set_order_status(request):
    order_id = request.GET.get('order_id')
    status = int(request.GET.get('status'))
    order = SalesOrder.objects.get(pk=order_id)
    if status == 1:
        order.status = 'PENDING'
        order.save()
    elif status == 2:
        order.status = 'SHIPPED'
        order.save()
    else:
        order.status = 'RECEIVED'
        order.save()
    test = "success"
    return sales_view(request, None, None, 'shipping-tab')
  
#This view is responsible for exporting reports on the history of sales order
@login_required(login_url='login')
def download_sales(request):
    items = SalesOrder.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales-history.csv"'
    writer = csv.writer(response, delimiter=',')
    #writing attributes
    #Find a way to get the attributes directly from the db
    writer.writerow(['Customer', 'Delivery date', 'Product', 'Quantity', 'Warehouse', 'Sale total', 'Status'])
    #writing data corresponding to attributes
    for obj in items:
        writer.writerow([obj.customer, obj.delivery_date, obj.product, obj.quantity, obj.warehouse, obj.sale_total, obj.status])
    return response

