from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """Concatenate arg1 and arg2."""
    return str(arg1) + str(arg2)