from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from dashboard.forms import CreateUserForm

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.manufacturing = reverse('manufacturing')
        self.register_url = reverse('register')
        self.validUser = {
            'username': 'testingUser',
            'email': 'testing@gmail.com',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }

    def test_manufacturing_GET(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)         
        response = self.client.get(self.manufacturing)     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'manufacturing.html')    