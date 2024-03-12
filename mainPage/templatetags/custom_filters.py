# custom_filters.py
from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key, None)

@register.filter
def get_array_value(dictionary, key, index):
    try:
        key = int(key)
        index = int(index)
        if key in dictionary and index < len(dictionary[key]):
            return dictionary[key][index]
        return None
    except (ValueError, TypeError):
        return None
    
@register.filter
def custom_range(value):
    return range(int(value))

@register.filter
def add_fullstop(value):
    if type(value) is str or type(value) is float :
        value = int(value)
    return format(value, ',d').replace(',', '.').strip('.')


@register.filter
def attr(widget, arg):
    kwargs = arg.split('=')
    widget['attrs'].update({kwargs[0]: kwargs[1]})
    return widget