from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def onload(script):
    html = f"<script>$(function(){{ {script} }});</script>"
    return mark_safe(html)