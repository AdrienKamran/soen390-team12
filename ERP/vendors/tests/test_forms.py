from django.test import TestCase
from vendors.forms import *
from inventory.models import *
from sales.models import *

class TestForms(TestCase):

    def test_VendorForm(self):
        form = VendorForm()
        data = {
            'v_name': 'Promark',
            'v_price_multiplier': 1.2,
            'v_address': '123 address', 
            'v_city': 'Montreal', 
            'v_province': 'Quebec', 
            'v_postal_code': 'h3b28k' 
        }
        form = VendorForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        filter_by_name = form.cleaned_data.get('v_name')
        self.assertEquals(filter_by_name, 'Promark')

    def test_VendorForm_already_exists(self):
        vendor = Vendor(v_name='Promark', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
        vendor.save()
        form = VendorForm()
        data = {
            'v_name': 'Promark',
            'v_price_multiplier': 1.2,
            'v_address': '123 address', 
            'v_city': 'Montreal', 
            'v_province': 'Quebec', 
            'v_postal_code': 'h3b28k' 
        }
        form = VendorForm(data)
        #Not valid cuz vendor's name already exists
        self.assertFalse(form.is_valid())

    def test_ReplenishMaterialForm(self):
        vendor = Vendor(v_name='Promark', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
        vendor.save()
        rawMaterial= Part(p_name='Steel', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Raw Material')
        rawMaterial.save()
        form = ReplenishMaterialForm()
        data = {
            'vendor': vendor,
            'part': rawMaterial,
            'quantity': 3
        }
        form = ReplenishMaterialForm(data)
        self.assertTrue(form.is_valid())


