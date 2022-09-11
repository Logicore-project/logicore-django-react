from django import template
from django.utils.safestring import SafeString
import requests, os, re
from django.conf import settings


register = template.Library()


@register.inclusion_tag("logicore_django_react/include_react_css.html")
def include_react_css(context):
    return {"FRONTEND_DEV_MODE": getattr(settings, "FRONTEND_DEV_MODE", False)}


@register.inclusion_tag("logicore_django_react/include_react_js.html")
def include_react_js(context):
    return {"FRONTEND_DEV_MODE": getattr(settings, "FRONTEND_DEV_MODE", False)}
