from django import template

register = template.Library()

@register.filter(name='group')
def group(u, group_names):
    group_names = group_names.split(',')
    return u.groups.filter(name__in=group_names).exists()
