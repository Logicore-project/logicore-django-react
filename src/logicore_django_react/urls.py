from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf import settings
from . import views
from pathlib import Path


bottom = [
    re_path(r'^(?P<path>.*)$', views.HomeView.as_view()) # XXX no comma at the end!
]


if getattr(settings, "FRONTEND_DEV_MODE", False):
    top = [
        re_path(r'^(?P<path>.*\.hot-update\.(js|json))$', views.hot_update), # \.[0-9a-z]{20}
        re_path('^react-static/(?P<path>.+)$', views.react_static)
    ]
else:
    top = [
        static("/react-static/", document_root=str(Path(settings.BASE_DIR) / "frontend" / "build" / "react-static"))
    ]
