from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

_form_id = "_postlinks_hidden_form"


@register.inclusion_tag("commons/tags/hiddenform.html")
def hiddenform():
    return {"id": _form_id, "action": "."}


@register.inclusion_tag("commons/tags/submit.js")
def submit(action):
    return {"id": _form_id, "action": action}


@register.inclusion_tag("commons/tags/onClick.html")
def submitOnClick(action):
    return {"action": render_to_string("commons/tags/submit.js", submit(action))}
