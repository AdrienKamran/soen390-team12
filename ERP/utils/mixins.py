from django import forms
from django.contrib.contenttypes.models import ContentType

from utils.models import Subscription


class NotifiableFormMixin(forms.Form):
    subscribe = forms.BooleanField(required=False)


class NotifiableViewMixin:

    def __init__(self):
        self.request = None

    def form_valid(self, form):
        super().form_valid(form)
        obj = form.instance
        if form.cleaned_data['subscribe']:
            sub = Subscription(
                user=self.request.user,
                object_id=obj.pk,
                content_type=ContentType.objects.get_for_model(obj)
            )
            sub.save()
        return super(NotifiableViewMixin, self).form_valid(form)
