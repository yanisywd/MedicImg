from django import template

register = template.Library()

@register.filter
def dictlookup(dictionary, key):
    return dictionary.get(key, 0)

@register.simple_tag
def get_value_from_dict(dictionary, key, attribute):
    return getattr(dictionary.get(key), attribute, None)