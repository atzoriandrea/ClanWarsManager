from django import template
from django.template.loader import render_to_string
from django.utils.html import mark_safe

register = template.Library()


@register.inclusion_tag("commons/tags/toast.html")
def toast(message, icon=None):
    return {"message": message, "icon": icon}

@register.simple_tag()
def toast_if(condition, message, icon=None):
    return mark_safe(render_to_string("commons/tags/toast.html", toast(message, icon)) if condition else "")
