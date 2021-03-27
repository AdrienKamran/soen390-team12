from django.views.generic import ListView

from utils.models import Notification


class NotificationViewList(ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 5
    ordering = '-timestamp'
