from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import View
from notifications.forms import SubscriptionForm
from notifications.models import Notification, Subscription

#A view that is responsible for displaying the notifications
class NotificationViewList(ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 5
    ordering = '-timestamp'

# A view that is responsible for creating subscription
class SubscriptionCreateView(View):
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        previous = request.POST.get('previous_page')
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.save()
        return HttpResponseRedirect(previous)

# A view that is responsible for deleting subscription
class SubscriptionDeleteView(View):
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        previous = request.POST.get('previous_page')
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            instance = form.save(commit=False)
            sub = Subscription.objects.get(content_type=instance.content_type, object_id=instance.object_id, user=instance.user)
            sub.delete()
        return HttpResponseRedirect(previous)