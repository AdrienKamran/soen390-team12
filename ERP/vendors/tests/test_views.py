from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from dashboard.forms import CreateUserForm
from vendors.forms import *

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.vendors = reverse('vendors')
        self.add_vendors = reverse('add-vendor')
        self.vendor_inventory = reverse('vendor-inventory')
        # self.delete_item = reverse('delete-inventory-part')
        self.replenish_inventory = reverse('add-rm')
        self.register_url = reverse('register')
        vendor = Vendor(v_name='Vendor2', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
        vendor.save()
        rawMaterial= Part(p_name='Steel', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Raw Material')
        rawMaterial.save()
        # item = SellsPart(v_FK=vendor, p_FK=rawMaterial, p_quantity=1)
        # item.save()
        self.validUser = {
            'username': 'testingUser',
            'email': 'testing@gmail.com',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }
        self.addVendorForm = {
            'v_name': 'Promark',
            'v_price_multiplier': 1.2,
            'v_address': '123 address', 
            'v_city': 'Montreal', 
            'v_province': 'Quebec', 
            'v_postal_code': 'h3b28k'
        }
        self.replenishRMForm = {
            'vendor': vendor,
            'part': rawMaterial,
            'quantity': 3
        }
        self.vendor_pk = {
            'vendor_id': vendor.pk
        }
        # self.item_pk = {
        #     'sellsPart_pk': item.pk
        # }

    def test_vendors_view_GET(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.get(self.vendors)     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors.html')

    def test_add_vendors_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.post(self.add_vendors, self.validUser, format='text/html')     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendors.html')

    def test_add_vendors_form_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)    
        response = self.client.post(self.add_vendors, self.addVendorForm, format='text/html')     
        self.assertEquals(response.status_code, 302)

    def test_replenish_rm_form_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)    
        response = self.client.post(self.replenish_inventory, self.replenishRMForm, format='text/html')     
        self.assertEquals(response.status_code, 200)


    def test_vendors_inventory_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)    
        response = self.client.post(self.vendor_inventory, self.vendor_pk, format='text/html')     
        self.assertEquals(response.status_code, 200)

    # def test_delete_item_POST(self):
    #     self.client.post(self.register_url, self.validUser, format='text/html')
    #     login_successful = self.client.login(username='testingUser', password="test123456!")
    #     self.assertTrue(login_successful)    
    #     response = self.client.post(self.delete_item, self.item_pk, format='text/html')     
    #     self.assertEquals(response.status_code, 200)