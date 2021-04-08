from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from dashboard.forms import CreateUserForm




class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
        self.validUser = {
            'username': 'testingUser',
            'email': 'testing@gmail.com',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }

        self.invalidUser = {
            'username': 'testingUser1',
            'email': 'Notvalid',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }
        
    def test_register_POST_validUser(self):
        response = self.client.post(self.register_url, self.validUser, format='text/html')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_register_POST_invalid_invalidUser(self):
        response = self.client.post(self.register_url, self.invalidUser, format='text/html')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        self.assertEquals(self.validUser.get('username'), 'testingUser')
        self.assertEquals(self.validUser.get('password1'), 'test123456!')
        user=User.objects.filter(username=self.validUser['username']).first()
        user.is_active=True
        user.save()
        response= self.client.post(self.login_url,self.validUser,format='text/html')
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/')

    def test_login_POST_invalidCred(self):
        self.client.post(self.register_url, self.validUser, format='text/html')        
        user=User.objects.filter(username=self.validUser['username']).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,self.invalidUser,format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_home_GET(self):
        self.client.post(self.register_url, self.validUser, format='text/html')
        login_successful = self.client.login(username='testingUser', password="test123456!")
        self.assertTrue(login_successful)        
        response = self.client.get(self.home_url)     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')