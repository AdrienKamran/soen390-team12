from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Part)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Vendor)
admin.site.register(SellsParts)
admin.site.register(Contains)
admin.site.register(MadeOf)
admin.site.register(Orders)
admin.site.register(OrderPart)
admin.site.register(Manufactures)
admin.site.register(ManufacturePart)

