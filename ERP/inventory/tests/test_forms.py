from django.test import TestCase
from inventory.forms import *
from inventory.models import *


class TestForms(TestCase):

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

    def test_CreateRawMaterialForm_valid(self):
        rm_form = CreateRawMaterialForm()
        data5 = {
            'p_name': 'Iron',
            'p_unit_value': 11.00,
            'p_type': 'Raw Material'
        }
        rm_form = CreateRawMaterialForm(data5)
        self.assertTrue(rm_form.is_valid())
        rm_form.save()
        raw_mat = rm_form.cleaned_data.get('p_name')
        self.assertEquals(raw_mat, 'Iron')

    def test_CreateNewVendorOfPartForm(self):
        form = CreateNewVendorOfPartForm()
        vendor = Vendor(v_name='Vendor1', v_price_multiplier=1.2, v_address='123 address', v_city='Montreal', v_province='Quebec', v_postal_code='h3b28k')
        part= Part(p_name='Steel', p_unit_value=10.00, p_size=2, p_color='Grey', p_finish='Matte', p_grade='Aluminum', p_type='Part')
        vendor.save()
        part.save()
        data = {
            'p_FK': part.pk,
            'v_FK': vendor.pk
        }
        form = CreateNewVendorOfPartForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        order_by_vendor = form.cleaned_data.get('v_FK')
        self.assertEquals(order_by_vendor, vendor)
        vendor.delete()
        part.delete()
            