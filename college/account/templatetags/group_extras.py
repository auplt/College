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


@register.simple_tag
def increment(data: int, inc: int):
    """
    Simple tag that increments variable.
    :param data: new value
    :param inc: increment value
    :return: variable with new value
    """
    return int(data) + int(inc)


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


@register.simple_tag
def change_query_string(query_string: str):
    """
    Simple tag that changes & in query string on :.
    :param query_string: input query string
    :return: variable with new value
    """
    return query_string.replace('&', ':')
