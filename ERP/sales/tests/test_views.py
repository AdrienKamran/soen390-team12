from django.test import TestCase, Client
from django.urls import reverse
from mixer.backend.django import mixer

from ..models import Customer


class TestViewsCase(TestCase):

    def setUp(self):

        self.valid_customer = {
            'name' : 'bob',
            'type' : 'Individual',
            'email' : 'bob@example.com',
            'phone_number' : '555555555',
            'address_line' : '123 fake street',
            'city' : 'montreal',
            'state' : 'quebec',
            'zip_code' : '5555',
            'country' : 'canada'
        }

        self.client = Client()

        self.customer = mixer.blend('sales.Customer')

        self.order = mixer.blend('sales.SalesOrder')

        self.product = mixer.blend('inventory.Product')

        self.warehouse = mixer.blend('inventory.Warehouse')

    def test_post_create_customer(self):
        response = self.client.post(reverse('add-customer'), self.valid_customer, format='text/html')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/sales')
