from django.db import models

from inventory.models import Product, Warehouse

class Customer(models.Model):
    type_choice = (
        ('company', 'company'),
        ('individual', 'individual')
    )
    name = models.TextField(max_length=256)
    type = models.TextField(choices=type_choice)
    email = models.EmailField()
    phone_number = models.TextField(max_length=256)
    address_line = models.TextField(max_length=256)
    city = models.TextField(max_length=256)
    state = models.TextField(max_length=256)
    zip_code = models.TextField(max_length=256)
    country = models.TextField(max_length=256)

class SalesOrder(models.Model):
    status_choice = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery_date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(max_length=10)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    sale_total = models.FloatField()
    status = models.TextField(choices=status_choice)
