import re

from django import template

register = template.Library()


@register.simple_tag
def active(request,pattern):
    if re.search(pattern,request.path):
        return 'selected'
    return ''

