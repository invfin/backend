from django.conf import settings


def general_settings(request):
    return {
        "debug": settings.DEBUG,
        "web_icon": settings.WEB_ICON,
        "webmanifest": settings.WEB_MANIFEST,
    }