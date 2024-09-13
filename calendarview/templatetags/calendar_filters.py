from django import template

register = template.Library()

@register.filter
def get_tasks(tasks_dict, day):
    """Custom template filter to get tasks for a given day."""
    
    return tasks_dict.get(day, [])
@register.filter
def split_string(value, separator=' '):
    """Splits a string by the given separator."""
    return value.split(separator)
@register.filter
def custom_truncatechars(value, max_length=50):
    """Custom filter to truncate a string to a maximum number of characters."""
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value