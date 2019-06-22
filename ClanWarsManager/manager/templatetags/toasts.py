from django import template
from .scripting import onload

register = template.Library()

@register.simple_tag()
def toast(message, icon=None):
    iconArg = "" if icon is None else f",'{icon}'"
    script = f"toast('{message}'{iconArg});"
    return onload(script)

@register.simple_tag
def toast_if(condition, message, icon=None):
    if condition:
        return toast(message, icon)