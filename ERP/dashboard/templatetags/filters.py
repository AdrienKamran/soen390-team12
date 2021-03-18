from django import template

register = template.Library()

@register.filter(name='group')
def group(u, group_names):
    group_names = group_names.split(',')
    return u.groups.filter(name__in=group_names).exists()

@register.filter(name='get_count')
def get_count(dictionary, key):
    return dictionary.get(key)

@register.filter(name='is_equal')
def is_equal(value_1, value_2):
	return value_1 == value_2