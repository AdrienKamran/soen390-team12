from django.db import models

from inventory.models import *

class Customer(models.Model):
    type_choice = (
        ('Company', 'Company'),
        ('Individual', 'Individual')
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100,choices=type_choice)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SalesOrder(models.Model):
    status_choice = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    date_created = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery_date = models.DateField()
    product = models.ForeignKey(Part, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    sale_total = models.FloatField()
    status = models.CharField(max_length=100,choices=status_choice)

class SalesPart(models.Model):
    s_FK = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    c_FK = models.ForeignKey(Contain, on_delete=models.CASCADE)
