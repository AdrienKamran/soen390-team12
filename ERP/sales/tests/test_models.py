from django.test import TestCase

from sales.models import Customer


class ModelTest(TestCase):

    def test_create_valid_customer(self):
        customer = Customer(
            name='bob',

        )