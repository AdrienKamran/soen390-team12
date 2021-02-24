from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from sample.forms import CreateUserForm


class TestCreateUserForm(TestCase):

    def test_form_valid(self):
        form = CreateUserForm()
        data = {
            'username': 'testingUser',
            'email': 'testing@gmail.com',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }

        form = CreateUserForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user = form.cleaned_data.get('username')
        self.assertEquals(user, 'testingUser')

    def test_form_invalid_email(self):
        form1 = CreateUserForm()

        data1 = {
            'username': 'testingUser',
            'email': 'notValid',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }

        form1 = CreateUserForm(data1)


        self.assertFalse(form1.is_valid())    

    def test_form_passwords_different(self):
        form2 = CreateUserForm()    
        data2 = {
            'username': 'testingUser',
            'email': 'testing.com',
            'password1': 'test123456!',
            'password2': '123456!',
        }

        form2 = CreateUserForm(data2)

        self.assertFalse(form2.is_valid())     

    def test_form_password_weak(self):
        form3 = CreateUserForm()
        data3 = {
            'username': 'testingUser',
            'email': 'testing.com',
            'password1': 'test',
            'password2': 'test',
        }

        form3 = CreateUserForm(data3)

        self.assertFalse(form3.is_valid())     