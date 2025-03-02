from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the argument."""
    return value * arg