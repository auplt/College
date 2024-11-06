import copy

from django import template
import ast
import datetime

from django.template.defaultfilters import stringfilter

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
def change_query_string(query_string: str) -> str | None:
    """
    Simple tag that changes & in query string on :.
    :param query_string: input query string
    :return: variable with new value
    """
    if not query_string:
        return None
    new_query_string = query_string.replace('&', ':')
    return new_query_string[:-1] if new_query_string[-1] == ':' else new_query_string


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
def create_tutors_dict(name: str, link: str) -> dict | None:
    """
    Simple tag that creates configuration dict for tt_lesson_details template.
    :param entity: input string with entity identifier name
    :param entity_id: input string with entity identifier value
    :param entity_name: input string with entity display name
    :except ValueError when string cannot be converted to dict
    :return: pyton dict ot None
    """
    print(name)
    try:
        return ast.literal_eval(
            f"{{'name': '{name}', 'link': '{str(link)}'}}")
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
    print(lst)
    if lst is None:
        lst = list()
    lst.append(copy.deepcopy(item))
    print(lst)
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


@register.simple_tag
def date_convertor(date_str: datetime.date) -> str:
    """
    Simple tag that converts date to '%d.%m.%Y' format.
    :param date_str: input date that should be converted
    :return: formatted date string
    """
    return date_str.strftime('%d.%m.%Y')


@register.simple_tag
def get_url_params(request) -> str | None:
    """
    Simple tag that returns parameters from input url without 'next' parameter.
    :param request: input request
    :return: string of url parameters without 'next' parameter
    """
    res_url = ""
    for key, value in request.GET.items():
        if res_url:
            res_url = res_url + '&'
        if key not in ('next', 'next_url'):
            res_url = res_url + key + '=' + value
    if res_url == "":
        return None
    return res_url


@register.filter
@stringfilter
def slicestring(value, arg):
    """usage: "mylongstring"|slicestring:"2:4" """
    els = list(map(int, arg.split(':')))
    # print(els)
    return value[els[0]:els[1]]

@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        print(some_list[int(current_index)])
        print(some_list[int(current_index) + 1])
        return some_list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception


@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) - 1] # access the previous element
    except:
        return '' # return empty string in case of exception
