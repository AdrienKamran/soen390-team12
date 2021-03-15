from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import *
from inventory import views as inventoryViews

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse ('home')
        self.assertEquals(resolve(url).func, home)

    def test_login_url_is_resolved(self):
        url = reverse ('login')
        self.assertEquals(resolve(url).func, loginPage)

    def test_register_url_is_resolved(self):
        url = reverse ('register')
        self.assertEquals(resolve(url).func, register)

    def test_logout_url_is_resolved(self):
        url = reverse ('logout')
        self.assertEquals(resolve(url).func, logoutUser)

    def test_generate_url_is_resolved(self):
        url = reverse ('generate')
        self.assertEquals(resolve(url).func, generateReport)

    def test_sales_url_is_resolved(self):
        url = reverse ('sales')
        self.assertEquals(resolve(url).func, salesViewPage)

    def test_manufacturing_url_is_resolved(self):
        url = reverse ('manufacturing')
        self.assertEquals(resolve(url).func, inventoryViews.manufacturingViewPage)

    def test_inventory_url_is_resolved(self):
        url = reverse ('inventory')
        self.assertEquals(resolve(url).func, inventory)                        

    def test_createmateriallist_url_is_resolved(self):
        url = reverse ('createMaterialList')
        self.assertEquals(resolve(url).func, inventoryViews.createMaterialList)

    def test_produceMaterialList_url_is_resolved(self):
        url = reverse ('produceMaterialList')
        self.assertEquals(resolve(url).func, inventoryViews.produceMaterialList)
    
    def test_manufacture_product_url_is_resolved(self):
        url = reverse ('manufacture-product')
        self.assertEquals(resolve(url).func, inventoryViews.manufactureProduct)

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
       