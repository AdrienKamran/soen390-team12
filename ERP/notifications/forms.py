from django import forms
from django.contrib.contenttypes.models import ContentType

from notifications.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['content_type', 'object_id']
        widgets = {
            'content_type': forms.HiddenInput,
            'object_id': forms.HiddenInput
        }


class SubscriptionCreateForm(SubscriptionForm):
    def save(self, commit=True):
        instance = super(SubscriptionCreateForm, self).save(commit=False)
        try:
            sub = Subscription.objects.get(instance)
        except Subscription.DoesNotExist:
            sub = Subscription.objects.create(instance)
        return sub


class SubscriptionDeleteForm(SubscriptionForm):
    def save(self, commit=True):
        try:
            sub = Subscription.objects.get(self.instance)
        except Subscription.DoesNotExist:
            return
        sub.delete()
