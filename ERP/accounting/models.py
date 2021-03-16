from django.db import models

# Create your models here.
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
    t_reference = models.IntegerField(default=0)