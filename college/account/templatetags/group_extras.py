from django import template

register = template.Library()


@register.simple_tag
def update_variable(data: any):
    """
    Simple tag that assigns new value to variable.
    :param data: new value
    :return: variable with new value
    """
    return data


@register.filter()
def is_number(value: any):
    """
    Filter that checks weather incoming value number or not.
    :param value: input value
    :return: True if incoming value is number, False otherwise
    """
    return value.isdigit()


@register.simple_tag
def get_value(dictionary: dict, data: str):
    """
    Simple tag that assigns new value to variable.
    :param dictionary: new value
    :param data: new value
    :return: variable with new value
    """
    return dictionary.get(data)
