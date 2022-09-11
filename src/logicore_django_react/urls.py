from django.urls import path, re_path, include
from django.conf import settings
from . import views


urlpatterns = [
    re_path(r'^(?P<path>.*)$', main_views.HomeView.as_view()),
]


if getattr(settings, "FRONTEND_DEV_MODE", False):
    urlpatterns = [
        re_path(r'^(?P<path>.*\.hot-update\.(js|json))$', views.hot_update), # \.[0-9a-z]{20}
        re_path('^react-static/(?P<path>.+)$', views.react_static),
    ] + urlpatterns
else:
    urlpatterns = [
        static("/react-static/", document_root=settings.BASE_DIR / "frontend" / "build" / "react-static")
    ] + urlpatterns
