from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def date_difference(value, arg):
    return value - arg
