from django import template
from django.utils.safestring import SafeString
import requests, os, re
from django.conf import settings
from .. import commons


register = template.Library()


@register.inclusion_tag("logicore_django_react/include_react_css.html")
def include_react_css():
    return {"FRONTEND_DEV_MODE": commons.FRONTEND_DEV_MODE}


@register.inclusion_tag("logicore_django_react/include_react_js.html")
def include_react_js():
    return {"FRONTEND_DEV_MODE": commons.FRONTEND_DEV_MODE}
