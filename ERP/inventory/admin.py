from django.contrib import admin
from .models import RawMaterials, Warehouse, ContainsRM, ContainsProducts, Products

# Register your models here.
admin.site.register(RawMaterials)
admin.site.register(Warehouse)
admin.site.register(ContainsRM)
admin.site.register(ContainsProducts)
admin.site.register(Products)