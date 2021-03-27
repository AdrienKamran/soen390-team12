from django import template
from django.utils.html import format_html

register = template.Library()


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


@register.inclusion_tag('get_notified.html')
def notify_widget(object):
    pass


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
