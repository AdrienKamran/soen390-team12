from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sales.views import *

class TestUrls(SimpleTestCase):

    def test_sales_url_is_resolved(self):
        url = reverse ('sales')
        self.assertEquals(resolve(url).func, sales_view)

    def test_sales_url_is_resolved(self):
        url = reverse ('add-customer')
        self.assertEquals(resolve(url).func, add_customer)

    def test_sales_url_is_resolved(self):
        url = reverse ('add-order')
        self.assertEquals(resolve(url).func, add_sale_order)        
