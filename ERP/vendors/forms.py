from django import forms
from django.forms import ModelChoiceField
from inventory.models import *

#To render the vendor names in ReplenishMaterialForm
class VendorModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.v_name

#To render the part names in ReplenishMaterialForm
class PartModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.p_name

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['v_name', 'v_price_multiplier', 'v_address', 'v_city', 'v_province', 'v_postal_code']

class ReplenishMaterialForm(forms.Form):
    vendor = VendorModelChoiceField(label='vendor Name', queryset=None)
    part = PartModelChoiceField(label='part name', queryset=None)
    quantity = forms.IntegerField(label='Quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor'].queryset = Vendor.objects.all()
        self.fields['part'].queryset = Part.objects.filter(p_type='Raw Material').all()