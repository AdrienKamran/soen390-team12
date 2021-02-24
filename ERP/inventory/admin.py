from django.contrib import admin
from .models import RawMaterials, Warehouse, ContainsRM, ContainsParts, Parts, Vendor, SellsRM,SellsParts, OrderRM, OrderParts

# Register your models here.
admin.site.register(RawMaterials)
admin.site.register(Warehouse)
admin.site.register(ContainsRM)
admin.site.register(ContainsParts)
admin.site.register(Parts)
admin.site.register(Vendor)
admin.site.register(SellsRM)
admin.site.register(SellsParts)
admin.site.register(OrderRM)
admin.site.register(OrderParts)