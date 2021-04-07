from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from notifications.forms import SubscriptionForm, SubscriptionCreateForm
from notifications.models import Subscription

register = template.Library()


def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user

    try:
        user_is_anonymous = user.is_anonymous()
    except TypeError:
        user_is_anonymous = user.is_anonymous

    if user_is_anonymous:
        return None
    return user


@register.simple_tag
def is_subscribed(user, obj):
    c_type = ContentType.objects.get_for_model(obj)
    try:
        Subscription.objects.get(
            user=user,
            content_type=c_type,
            object_id=obj.pk
        )
    except Subscription.DoesNotExist:
        return False
    return True


@register.simple_tag(takes_context=True)
def unread_notifications_count(context):
    user = user_context(context)
    if not user:
        return ''
    return user.notifications.unread().count()


@register.simple_tag
def has_notification(user):
    if user:
        return user.notifications.unread().exists()


@register.simple_tag(takes_context=True)
def notification_badge(context):
    user = user_context(context)
    if not user:
        return ''

    html = "<span class='badge'>{unread_count}</span>".format(
        unread_count=user.notifications.unread().count()
    )
    return format_html(html)


@register.inclusion_tag('notification_list.html', takes_context=True)
def notification_menu(context):
    user = user_context(context)
    if not user:
        return ''
    notification_count = user.notifications.unread().count()
    return {'notifications': user.notifications.unread(),
            'notification_count': notification_count}


@register.inclusion_tag('get_notified.html', takes_context=True)
def notify_widget(context, obj):
    user = user_context(context)
    if not user:
        return ''
    data = {'content_type': ContentType.objects.get_for_model(obj), 'object_id': obj.pk}
    form = SubscriptionForm(data)
    return {'obj': obj, 'form': form, 'user': user, 'request': context.get('request')}
