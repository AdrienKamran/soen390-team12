from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from dashboard.forms import CreateUserForm
from inventory.models import *
from sales.models import *

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.sales = reverse('sales')
        self.add_customer = reverse('add-customer')
        self.add_order = reverse('add-order')
        self.register_url = reverse('register')
        self.validUser = {
            'username': 'testingUser',
            'email': 'testing@gmail.com',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }
        self.addCustomerForm = {
            'name': 'Jackson',
            'type': 'Individual',
            'email': 'jackson@jackson.com', 
            'phone_number': 1234567891, 
            'address_line': '123 address', 
            'city': 'Montreal', 
            'state': 'Quebec', 
            'zip_code': 'h3b28k', 
            'country': 'Canada'
        }

    def test_sales_GET(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.get(self.sales)     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales.html')

    def test_add_customer_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.post(self.add_customer, self.validUser, format='text/html')     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales.html')

    def test_add_customer_form_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)    
        response = self.client.post(self.add_customer, self.addCustomerForm, format='text/html')     
        self.assertEquals(response.status_code, 302)

    def test_add_order_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.post(self.add_order, self.validUser, format='text/html')     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales.html')                    
