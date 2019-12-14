from django import template

register = template.Library()


# @register.simple_tag
# def multiply(qty, simbol):
#     return qty * simbol


@register.filter
def to_star(qty):
    return str(qty * '★')
