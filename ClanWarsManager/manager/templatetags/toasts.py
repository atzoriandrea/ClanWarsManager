from django import template
from django.utils.html import mark_safe
from .scripting import onload

register = template.Library()

@register.simple_tag()
def toast(message, icon=None):
    iconArg = "" if icon is None else f",'{icon}'"
    script = f"toast('{message}'{iconArg});"
    return onload(script)

@register.simple_tag
def toast_if(condition, message, icon=None):
    return mark_safe(toast(message, icon) if condition else "")
