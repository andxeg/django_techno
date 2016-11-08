from django import template

register = template.Library()


@register.simple_tag
def convert_to_string_and_concate(arg1, arg2):
    return str(arg1) + str(arg2)
