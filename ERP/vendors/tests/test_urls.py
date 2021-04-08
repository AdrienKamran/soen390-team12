from django.test import SimpleTestCase
from django.urls import reverse, resolve
from vendors.views import *

class TestUrls(SimpleTestCase):
    
    def test_vendors_view_url_is_resolved(self):
        url = reverse ('vendors')
        self.assertEquals(resolve(url).func, vendors_view)

    def test_add_vendor_url_is_resolved(self):
        url = reverse ('add-vendor')
        self.assertEquals(resolve(url).func, add_vendor)

    def test_vendors_inventory_url_is_resolved(self):
        url = reverse ('vendor-inventory')
        self.assertEquals(resolve(url).func, vendors_inventory)

    def test_delete_item_url_is_resolved(self):
        url = reverse ('delete-vendor-part')
        self.assertEquals(resolve(url).func, delete_item)

    def test_replenish_inventory_url_is_resolved(self):
        url = reverse ('add-rm')
        self.assertEquals(resolve(url).func, replenish_inventory)        