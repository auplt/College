import copy

from django import template
import ast

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


@register.simple_tag
def original_query_string(query_string: str):
    """
    Simple tag that changes : in changed query string on &.
    :param query_string: input changed query string
    :return: variable with new value
    """
    return query_string.replace(':', '&')


@register.simple_tag
def create_tt_conf_dict(entity: str, entity_id: str, entity_name: str) -> dict | None:
    """
    Simple tag that creates configuration dict for tt_lesson_details template.
    :param entity: input string with entity identifier name
    :param entity_id: input string with entity identifier value
    :param entity_name: input string with entity display name
    :except ValueError when string cannot be converted to dict
    :return: pyton dict ot None
    """
    try:
        return ast.literal_eval(
            f"{{'entity': '{entity}', 'entity_id': {str(entity_id)}, 'entity_name': '{entity_name}'}}")
    except ValueError:
        return None


@register.simple_tag
def add_to_list(item, lst=None) -> list:
    """
    Simple tag that adds item to list if there is no list, it creates the new one.
    :param item: input item that should be added
    :param lst: input list where item should be added
    :return: list with new item
    """
    if lst is None:
        lst = list()
    lst.append(copy.deepcopy(item))
    return lst


@register.filter
def get_type(value: any) -> str:
    """
    Filter that returns class name
    :param value: input value which class is needed to be returned
    :return: class name
    """
    return type(value).__name__


@register.filter
def add_str(arg1, arg2):
    """
    Filter that concatenates two strings
    :param arg1: input string to which string will be added
    :param arg2: input string that would be added
    :return: concatenated input strings
    """
    return str(arg1) + str(arg2)
