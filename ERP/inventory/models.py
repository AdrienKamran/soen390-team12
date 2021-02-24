from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class TestModel(models.Model):
    field1 = models.CharField(max_length=80)
    field2 = models.IntegerField()


class Parts(models.Model):
    p_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    p_unit_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)

class RawMaterials(models.Model):
    rm_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    rm_unit_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)


class Warehouse(models.Model):
    w_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    w_address = models.CharField(max_length=120)
    w_city = models.CharField(max_length=120)
    w_province = models.CharField(max_length=120)
    w_postal_code = models.CharField(max_length=6)

class MadeOfRM(models.Model):
    part_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    rm_quantity = models.IntegerField(default=1, null=False, blank=False)

class MadeOfParts(models.Model):
    part_1_FK = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name='%(class)s_parent_product')
    part_2_FK = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name='%(class)s_child_part')
    p_quantity = models.IntegerField(default=1, null=False, blank=False)

class ContainsRM(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    rm_FK = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    rm_quantity = models.IntegerField(default=1, null=False, blank=False)

class ContainsParts(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product_FK = models.ForeignKey(Parts, on_delete=models.CASCADE)
    p_quantity = models.IntegerField(default=1, null=False, blank=False)
