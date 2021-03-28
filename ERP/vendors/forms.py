from django import forms
from inventory.models import *

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['v_name', 'v_price_multiplier', 'v_address', 'v_city', 'v_province', 'v_postal_code']