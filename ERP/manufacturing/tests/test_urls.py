from django.test import SimpleTestCase
from django.urls import reverse, resolve
from manufacturing.views import *

class TestUrls(SimpleTestCase):

    def test_manufacturing_url_is_resolved(self):
        url = reverse ('manufacturing')
        self.assertEquals(resolve(url).func, manufacturingViewPage)

    def test_createmateriallist_url_is_resolved(self):
        url = reverse ('createMaterialList')
        self.assertEquals(resolve(url).func, createMaterialList)

    def test_produceMaterialList_url_is_resolved(self):
        url = reverse ('produceMaterialList')
        self.assertEquals(resolve(url).func, produceMaterialList)
    
    def test_manufacture_product_url_is_resolved(self):
        url = reverse ('manufacture-product')
        self.assertEquals(resolve(url).func, manufactureProduct) 

    def test_loadMaterialList_url_is_resolved(self):
        url = reverse ('loadMaterialList')
        self.assertEquals(resolve(url).func, loadMaterialList)           