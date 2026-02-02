from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely get dictionary item, return empty list if key missing."""
    if dictionary is None:
        return []
    return dictionary.get(key, [])

