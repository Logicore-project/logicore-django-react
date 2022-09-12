from django.views.generic import TemplateView
from proxy.views import proxy_view
from django.conf import settings


class HomeView(TemplateView):
    template_name = getattr(
        settings,
        "LOGICORE_DJANGO_REACT_TEMPLATE",
        "logicore_django_react/home.html"
    )


port = getattr(settings, "LOGICORE_DJANGO_REACT_PORT", 3000)


def react_static(request, path):
    if path.lower().endswith(".css") or path.lower().endswith(".js"):
        remoteurl = f"http://127.0.0.1:{port}/static/" + path
    else:
        remoteurl = f"http://127.0.0.1:{port}/react-static/" + path
    return proxy_view(request, remoteurl, {})


def hot_update(request, path):
    remoteurl = f"http://127.0.0.1:{port}/" + path
    return proxy_view(request, remoteurl, {})
