from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf import settings
from . import views, commons
from pathlib import Path
from django.conf.urls.i18n import i18n_patterns


react_html_template_urls = [
    *i18n_patterns(re_path(r'^(?P<path>.*)$', views.HomeView.as_view()), prefix_default_language=False),
]


if commons.FRONTEND_DEV_MODE:
    react_reload_and_static_urls = [
        re_path(r'^(?P<path>.*\.hot-update\.(js|json))$', views.hot_update), # \.[0-9a-z]{20}
        re_path('^react-static/(?P<path>.+)$', views.react_static),
    ]
else:
    react_reload_and_static_urls = static("/react-static/", document_root=str(Path(settings.BASE_DIR) / "frontend" / "build" / "react-static"))
