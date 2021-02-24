from django import template

register = template.Library()

@register.filter(name='calculateCost')
def calculate_cost(value, args):
    string_args = str(args)
    args_list = string_args.split(",")
    arg1 = int(args_list[0])
    #arg2 = float(args_list[1])
    return value

@register.filter(name='addString')
def add_string(value, arg):
    return f"{value}, {arg}"