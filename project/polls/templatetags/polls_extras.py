from django import template

register = template.Library()


@register.simple_tag
def convert_to_string(*args):
    result = ""
    for arg in args:
        result = result + str(arg)

    return result
