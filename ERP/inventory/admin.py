from django.contrib import admin
from .models import RawMaterials, Warehouse, ContainsRM, ContainsParts, Parts

# Register your models here.
admin.site.register(RawMaterials)
admin.site.register(Warehouse)
admin.site.register(ContainsRM)
admin.site.register(ContainsParts)
admin.site.register(Parts)