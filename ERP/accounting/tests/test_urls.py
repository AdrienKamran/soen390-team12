from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounting.views import *

class TestUrls(SimpleTestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse ('accounting')
        self.assertEquals(resolve(url).func, accounting)
