from django.db import models

# Create your models here.
'''

'''
class Part(models.Model):
    finish_choices = (
        ('Matte', 'Matte'),
        ('Glossy', 'Glossy'),
        ('Chrome', 'Chrome')
    )
    grade_choices = (
        ('Aluminum', 'Aluminum'),
        ('Steel', 'Steel'),
        ('Carbon', 'Carbon')
    )
    type_choices = (
        ('Raw Material', 'Raw Material'),
        ('Part', 'Part'),
        ('Product', 'Product')
    )
    p_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    p_unit_value = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=9)
    p_size = models.IntegerField(null=True, blank=True, default=1)
    p_color = models.CharField(null=True, blank=True, max_length=7, unique=True)
    p_finish = models.TextField(choices=finish_choices, null=True, blank=True, default='Glossy')
    p_grade = models.TextField(choices=grade_choices, null=True, blank=True, default='Aluminum')
    p_type = models.TextField(choices=type_choices, null=False, blank=False, default='Part')

    def __str__(self):
		    return self.p_name

'''

'''
class Product(models.Model):
    type_choices = (
        ('Mountain Bike', 'Mountain Bike'),
        ('Road Bike', 'Road Bike'),
        ('Hybrid Bike', 'Hybrid Bike')
    )
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    selling_price = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    prod_type = models.TextField(choices=type_choices, null=False, blank=False, default='Hybrid Bike')
    prod_weight = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)

    def __str__(self):
		    return self.p_FK.p_name + " " + self.type_choices 

'''

'''
class Warehouse(models.Model):
    w_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    w_address = models.CharField(max_length=120)
    w_city = models.CharField(max_length=120)
    w_province = models.CharField(max_length=120)
    w_postal_code = models.CharField(max_length=6)

    def __str__(self):
		    return self.w_name
'''

'''
class Vendor(models.Model):
    v_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    v_price_multiplier = models.DecimalField(decimal_places=5, null=False, blank=False, max_digits=9)
    v_address = models.CharField(max_length=120)
    v_city = models.CharField(max_length=120)
    v_province = models.CharField(max_length=120)
    v_postal_code = models.CharField(max_length=6)

    def __str__(self):
		    return self.v_name
'''
Table containing the material is that describes the sub-parts making up parts and products.
'''
class MadeOf(models.Model):
    part_FK_parent = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='%(class)s_parent_part')
    part_FK_child = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='%(class)s_child_part')
    quantity = models.IntegerField()

    def __str__(self):
		    return self.part_FK_parent.p_name
'''

'''
class Contains(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    p_defective = models.BooleanField(null=False, blank=False, default=False)
    p_serial = models.BigIntegerField(default=10000)

    def __str__(self):
		    return self.w_FK.w_name + " " + self.p_FK.p_name + " " + str(self.p_serial)
'''

'''
class SellsParts(models.Model):
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    p_quantity = models.IntegerField(default=100, null=False, blank=False)

    def __str__(self):
            return self.v_FK.v_name + " " + self.p_FK.p_name

'''

'''
class Orders(models.Model):
    status_choices = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_status = models.TextField(choices=status_choices, null=False, blank=False, default='PENDING')
    order_quantity = models.IntegerField(default=1, null=False, blank=False)
    order_total_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
            return self.v_FK.v_name + " " + self.p_FK.p_name + " " + str(self.order_quantity) + " " + self.order_status