from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from dashboard.forms import *
from inventory.models import *


class TestCreateUserForm(TestCase):

    def test_Userform_valid(self):
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

    def test_Userform_invalid_email(self):
        form1 = CreateUserForm()

        data1 = {
            'username': 'testingUser',
            'email': 'notValid',
            'password1': 'test123456!',
            'password2': 'test123456!',
        }

        form1 = CreateUserForm(data1)


        self.assertFalse(form1.is_valid())    

    def test_Userform_passwords_different(self):
        form2 = CreateUserForm()    
        data2 = {
            'username': 'testingUser',
            'email': 'testing.com',
            'password1': 'test123456!',
            'password2': '123456!',
        }

        form2 = CreateUserForm(data2)

        self.assertFalse(form2.is_valid())     

    def test_Userform_password_weak(self):
        form3 = CreateUserForm()
        data3 = {
            'username': 'testingUser',
            'email': 'testing.com',
            'password1': 'test',
            'password2': 'test',
        }

        form3 = CreateUserForm(data3)

        self.assertFalse(form3.is_valid())

    def test_OrderRMform_valid(self):
        form = OrderRawMaterialForm()
        vendor = Vendor(v_name='Vendor1', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
        rawMaterial= Part(p_name='Steel', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Raw Material')
        warehouse = Warehouse(w_name='Warehouse1', w_address='456 address', w_city='Montreal', w_province='Quebec', w_postal_code='h3b28k')
        vendor.save()
        rawMaterial.save()
        warehouse.save()
        data = {
            'v_FK': vendor.pk,
            'p_FK': rawMaterial.pk,
            'w_FK': warehouse.pk,
            'order_quantity': 2,
            'order_total_cost' : 24.00
        }
        form = OrderRawMaterialForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        order_by_vendor = form.cleaned_data.get('v_FK')
        self.assertEquals(order_by_vendor, vendor)
        vendor.delete()
        rawMaterial.delete()
        warehouse.delete()

    # def test_CreateRawMaterialForm_valid(self):
    #     rm_form = CreateRawMaterialForm()
    #     rawMaterial1= Part(p_name='Rubber', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Raw Material')
    #     # vendor = Vendor(v_name='Vendor1', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
    #     rawMaterial1.save()
    #     data5 = {
    #         'p_name': rawMaterial1.p_name,
    #         'p_unit_value': rawMaterial1.p_unit_value,
    #         'p_type': 'Raw Material'
    #     }
    #     rm_form = CreateRawMaterialForm(data5)
    #     self.assertTrue(rm_form.is_valid())
    #     rm_form.save()
    #     raw_mat = rm_form.cleaned_data.get('p_name')
    #     self.assertEquals(raw_mat, 'Rubber')