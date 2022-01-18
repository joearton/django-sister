import inspect
from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def get_dict_value(obj_dict, dict_key):
    output = obj_dict.get(dict_key)
    if isinstance(dict_key, list):
        output = obj_dict.get(dict_key[0])
        output = output.get(dict_key[1])
    return output


@register.filter
def get_list_index(obj_list, index):
    index = int(index)
    return obj_list[index]


@register.filter
def pb_value(obj):
    if type(obj) == str:
        if obj.isdigit():
            obj = int(obj)
    if type(obj) == float:   
        obj = int(obj)
    return str(obj).replace('.', ',')


@register.filter
def in_group(user, group_names):
    return user.groups.filter(name__in=group_names).exists()


@register.filter
def field_name(field):
    return field.__class__.__name__


@register.filter
def get_dir(obj):
    return dir(obj)


@register.filter
def get_field(obj, attr):
    field = getattr(obj, attr)
    if inspect.ismethod(field):
        return field()
    return field


@register.filter
def th_title(obj):
    for index in ['get', '_']:
        obj = obj.replace(index, ' ')
    return obj.title()


@register.filter
def reverse_url(url_name):
    try:
        return reverse(url_name)
    except:
        return url_name


@register.filter
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])