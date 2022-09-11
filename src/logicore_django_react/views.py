


class HomeView(TemplateView):
    template_name = "home.html"


def react_static(request, path):
    if path.lower().endswith(".css") or path.lower().endswith(".js"):
        remoteurl = "http://127.0.0.1:3000/static/" + path
    else:
        remoteurl = "http://127.0.0.1:3000/react-static/" + path
    return proxy_view(request, remoteurl, {})


def hot_update(request, path):
    remoteurl = "http://127.0.0.1:3000/" + path
    return proxy_view(request, remoteurl, {})
