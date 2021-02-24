from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class TestModel(models.Model):
    field1 = models.CharField(max_length=80)
    field2 = models.IntegerField()

class Products(models.Model):
    type_choices = (
        ('Mountain Bike', 'Mountain Bike'),
        ('Road Bike', 'Road Bike'),
        ('Hybrid Bike', 'Hybrid Bike')
    )
    size_choices = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large')
    )
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
    prod_type = models.TextField(choices=type_choices, null=False, blank=False, default='Hybrid Bike')
    prod_weight = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    prod_model = models.CharField(null=False, blank=False, max_length=10, unique=True)
    prod_size = models.TextField(choices=size_choices, null=False, blank=False, default='Medium')
    prod_color = models.CharField(null=False, blank=False, max_length=7, unique=True)
    prod_finish = models.TextField(choices=finish_choices, null=False, blank=False, default='Glossy')
    prod_grade = models.TextField(choices=grade_choices, null=False, blank=False, default='Aluminum')

class Parts(models.Model):
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
    p_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    p_unit_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    p_size = models.IntegerField(null=False, blank=False, default=1)
    p_color = models.CharField(null=False, blank=False, max_length=7, unique=True)
    p_finish = models.TextField(choices=finish_choices, null=False, blank=False, default='Glossy')
    p_grade = models.TextField(choices=grade_choices, null=False, blank=False, default='Aluminum')

class RawMaterials(models.Model):
    rm_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    rm_unit_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)


class Warehouse(models.Model):
    w_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    w_address = models.CharField(max_length=120)
    w_city = models.CharField(max_length=120)
    w_province = models.CharField(max_length=120)
    w_postal_code = models.CharField(max_length=6)

class Vendor(models.Model):
    v_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    v_price_multiplier = models.DecimalField(decimal_places=5, null=False, blank=False, max_digits=9)
    v_address = models.CharField(max_length=120)
    v_city = models.CharField(max_length=120)
    v_province = models.CharField(max_length=120)
    v_postal_code = models.CharField(max_length=6)

class MadeOfRM(models.Model):
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    rm_quantity = models.IntegerField(default=1, null=False, blank=False)

class MadeOfSubParts(models.Model):
    part_1_FK = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name='%(class)s_parent_product')
    part_2_FK = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name='%(class)s_child_part')
    p_quantity = models.IntegerField(default=1, null=False, blank=False)

class MadeOfParts(models.Model):
    product_FK = models.ForeignKey(Products, on_delete=models.CASCADE)
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    part_quantity = models.IntegerField(default=1, null=False, blank=False)

class ContainsRM(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    rm_quantity = models.IntegerField(default=1, null=False, blank=False)

class ContainsParts(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    part_quantity = models.IntegerField(default=1, null=False, blank=False)

class ContainsProducts(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product_FK = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1, null=False, blank=False)

class SellsParts(models.Model):
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    part_quantity = models.IntegerField(default=1, null=False, blank=False)

class SellsRM(models.Model):
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    rm_quantity = models.IntegerField(default=1, null=False, blank=False)

class OrderParts(models.Model):
    status_choices = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_status = models.TextField(choices=status_choices, null=False, blank=False, default='PENDING')
    order_quantity = models.IntegerField(default=1, null=False, blank=False)
    order_total_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)

class OrderRM(models.Model):
    status_choices = (
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('RECEIVED', 'RECEIVED')
    )
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_status = models.TextField(choices=status_choices, null=False, blank=False, default='PENDING')
    order_quantity = models.IntegerField(default=1, null=False, blank=False)
    order_total_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)