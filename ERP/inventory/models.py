from django.db import models

# Model that references the template of a raw material, part or product. Each item in the inventory
# references a template in this model.
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

# Model that keeps the list of vendors to buy raw material from. Vendors can only sell raw materials.
class Vendor(models.Model):
    v_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    v_price_multiplier = models.DecimalField(decimal_places=5, null=False, blank=False, max_digits=9)
    v_address = models.CharField(max_length=120)
    v_city = models.CharField(max_length=120)
    v_province = models.CharField(max_length=120)
    v_postal_code = models.CharField(max_length=6)

    def __str__(self):
            return self.v_name

# Model that creates the relationship between the vendors and the parts they sell as well as how many of those
# parts they have in stock
class SellsPart(models.Model):
    v_FK = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    p_quantity = models.IntegerField(default=100, null=False, blank=False)

    def __str__(self):
            return self.v_FK.v_name + " " + self.p_FK.p_name

# Model that keeps a record of every product. Only parts of type "PRODUCT" can appear in this table.
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

# Model that keeps a list of warehouses.
class Warehouse(models.Model):
    w_name = models.CharField(null=False, blank=False, max_length=80, unique=True)
    w_address = models.CharField(max_length=120)
    w_city = models.CharField(max_length=120)
    w_province = models.CharField(max_length=120)
    w_postal_code = models.CharField(max_length=6)

    def __str__(self):
		    return self.w_name

# Effectively the inventory for every warehouse. This models tracks every distinct part, sub-part, raw material and products that
# that each warehouse has in inventory
class Contain(models.Model):
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    p_defective = models.BooleanField(null=False, blank=False, default=False)
    p_serial = models.BigIntegerField(default=10000)
    p_in_inventory = models.BooleanField(default=False)

    def __str__(self):
		    return self.w_FK.w_name + " " + self.p_FK.p_name + " " + str(self.p_serial)

# Model that tracks the orders created by the user. This tracks orders of raw materials only.
class Order(models.Model):
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

# Model that links the specific part created in the contains model to the order that created it.
class OrdersPart(models.Model):
    o_FK = models.ForeignKey(Order, on_delete=models.CASCADE)
    c_FK = models.ForeignKey(Contain, on_delete=models.CASCADE)


