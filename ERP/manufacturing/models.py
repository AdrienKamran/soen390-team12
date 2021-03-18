from django.db import models

from inventory.models import Warehouse, Contain, Part, Vendor

# Model that tracks the manufacturing orders. Every time a part or product is manufactured, a record
# gets created in here to keep a history.
class Manufacture(models.Model):
    p_FK = models.ForeignKey(Part, on_delete=models.CASCADE)
    w_FK = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    manufacture_quantity = models.IntegerField(default=1, null=False, blank=False)
    manufacture_total_cost = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
            return self.w_FK.w_name + " " + self.p_FK.p_name + " " + str(self.manufacture_quantity) + " "

# Model that links the specific sub-parts that make up a larger part or product. This is for tracking and history
# purposes.
class ManufacturesPart(models.Model):
    m_FK = models.ForeignKey(Manufacture, on_delete=models.CASCADE)
    c_FK = models.ForeignKey(Contain, on_delete=models.CASCADE)

# Model stores the sub-parts that make up a larger part or product. This table is relatively the material lists. It consists of
# all the parts <-> sub-parts relationships, effectively a material list
class MadeOf(models.Model):
    part_FK_parent = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='%(class)s_parent_part')
    part_FK_child = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='%(class)s_child_part')
    quantity = models.IntegerField()

    def __str__(self):
		    return self.part_FK_parent.p_name
