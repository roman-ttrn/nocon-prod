from django import template

register = template.Library()

@register.filter
def css_class(value):
    return value.lower().replace(" ", "-")
