from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Part)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Vendor)
admin.site.register(SellsPart)
admin.site.register(Contain)
admin.site.register(Order)
admin.site.register(OrdersPart)
