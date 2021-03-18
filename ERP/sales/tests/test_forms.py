from django.test import TestCase
from sales.forms import *
from inventory.models import *
from sales.models import *


class TestSalesForms(TestCase):

    # def test_OrderForm(self):
    #     form = OrderForm()
    #     cust = Customer(name='Mike', type='Individual', email='mike@mike.com', phone_number=1234567891, address_line='123 address', city='Montreal', state='Quebec', zip_code='h3b28k', country='Canada')
    #     part= Part(p_name='bike23', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Product')
    #     product = Product(p_FK=part, selling_price=400.50, prod_type='Mountain Bike', prod_weight=12.88)
    #     warehouse = Warehouse(w_name='Warehouse1', w_address='456 address', w_city='Montreal', w_province='Quebec', w_postal_code='h3b28k')
    #     sales_order= SalesOrder(customer=cust, delivery_date='2022-02-01', product=product , quantity=4, warehouse=warehouse , sale_total=300.23, status='PENDING')
    #     cust.save()
    #     part.save()
    #     product.save()
    #     warehouse.save()
    #     sales_order.save()

    #     data = {
    #             'customer': cust.pk,
    #             'delivery_date': '01-02-2022',
    #             'product': product.pk,
    #             'quantity' : 4,
    #             'warehouse': warehouse.pk,
    #             'status': 'PENDING'
    #         }
    #     form = OrderForm(data)
    #     self.assertTrue(form.is_valid())
    #     form.save()
    #     filter_by_cust = form.cleaned_data.get('customer')
    #     self.assertEquals(filter_by_cust, cust)
    #     # vendor.delete()
    #     # rawMaterial.delete()
    #     # warehouse.delete()

    def test_CustomerForm(self):
        form = CustomerForm()
        cust = Customer(name='Mike', type='Individual', email='mike@mike.com', phone_number=1234567891, address_line='123 address', city='Montreal', state='Quebec', zip_code='h3b28k', country='Canada')
        cust.save()
        data = {
            'name': 'Mike',
            'type': 'Individual',
            'email': 'mike@mike.com', 
            'phone_number': 1234567891, 
            'address_line': '123 address', 
            'city': 'Montreal', 
            'state': 'Quebec', 
            'zip_code': 'h3b28k', 
            'country': 'Canada'
        }
        form = CustomerForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        filter_by_name = form.cleaned_data.get('name')
        self.assertEquals(filter_by_name, cust.name)

