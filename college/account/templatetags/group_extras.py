from django import template

register = template.Library()


@register.simple_tag
def update_variable(data):
    return data
