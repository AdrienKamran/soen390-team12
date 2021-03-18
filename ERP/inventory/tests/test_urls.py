from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inventory.views import *

class TestUrls(SimpleTestCase):
    
    def test_inventory_url_is_resolved(self):
        url = reverse ('inventory')
        self.assertEquals(resolve(url).func, inventory)

    def test_return_raw_material_url_is_resolved(self):
        url = reverse ('return-raw-material')
        self.assertEquals(resolve(url).func, returnRawMaterial)

    def test_order_raw_material_url_is_resolved(self):
        url = reverse ('order-raw-material')
        self.assertEquals(resolve(url).func, orderRawMaterial)

    def test_create_raw_material_url_is_resolved(self):
        url = reverse ('create-raw-material')
        self.assertEquals(resolve(url).func, createRawMaterial)

    def test_checkUniqueRawMatName_url_is_resolved(self):
        url = reverse ('check-unique')
        self.assertEquals(resolve(url).func, checkUniqueRawMatName) 

    def test_return_vendor_url_is_resolved(self):
        url = reverse ('return-vendor')
        self.assertEquals(resolve(url).func, returnVendor)

    def test_inventory_part_url_is_resolved(self):
        url = reverse ('inventory-part')
        self.assertEquals(resolve(url).func, inventoryPartView)

    def test_toggle_inventory_part_status_url_is_resolved(self):
        url = reverse ('toggle-inventory-part-status')
        self.assertEquals(resolve(url).func, toggleInventoryPartStatus)

    def test_delete_inventory_part_url_is_resolved(self):
        url = reverse ('delete-inventory-part')
        self.assertEquals(resolve(url).func, deleteInventoryPart)
                            
