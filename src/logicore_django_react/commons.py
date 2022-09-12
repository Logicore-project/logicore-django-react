from django.conf import settings

try:
    FRONTEND_DEV_MODE = settings.FRONTEND_DEV_MODE
except AttributeError:
    raise ImporperlyConfigured("No FRONTEND_DEV_MODE found in Django settings. To use logicore_django_react, please add it, e.g. FRONTEND_DEV_MODE = os.environ.get(\"FRONTEND_DEV_MODE\", False)")
