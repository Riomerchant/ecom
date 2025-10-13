# templatetags/cart_extras.py
from django import template
register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg




@register.filter
def tot(value, arg):
    return value+(value*(18/100))