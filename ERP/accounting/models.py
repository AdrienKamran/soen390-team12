from django.db import models
"""
    Wrapper model for the 3 different types of transactions, ORDER, MANUFACTURE AND SALE. This table is used so that
    the cost and profit information can be neatly displayed in one table. A transaction is created after every sale, after
    every part/product manufactured and after every order.
"""
class Transaction(models.Model):
    type_choices = (
        ('ORDER', 'ORDER'),
        ('MANUFACTURE', 'MANUFACTURE'),
        ('SALE', 'SALE')
    )
    t_type = models.TextField(choices=type_choices, null=False, blank=False, default='ORDER')
    t_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    t_balance = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    t_item_name = models.CharField(max_length=100, null=False, blank=False)
    t_serial = models.BigIntegerField(default=500000, null=False, blank=False)
    t_quantity = models.IntegerField(default=0, null=False, blank=False)
