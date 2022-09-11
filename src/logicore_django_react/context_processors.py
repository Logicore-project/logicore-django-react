from django.conf import settings


def react(request):
    return {
        'FRONTEND_DEV_MODE': settings.get("FRONTEND_DEV_MODE", False),
        "test": "2-hf-13hf340=34hj034",
    }
