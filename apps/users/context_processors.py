from django.conf import settings
from django.contrib.auth import get_user_model

from apps.notifications.models import Notification

User = get_user_model()


def users_notifications(request):
    user = request.user
    count_notifications = 0
    user_notifs = None
    # TODO ask for request.auth, if it's found it means that it comes from API
    try:
        if user.is_authenticated:
            user_notifs = Notification.objects.filter(user=user).order_by("-date")
            count_notifications = user_notifs.count()
        return {"count_notifications": count_notifications, "user_notifs": user_notifs}
    except Exception:
        pass
    return {}


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def user_companies_visited(request):
    companies_visited = []
    if "companies_visited" in request.session:
        companies_visited = request.session["companies_visited"]
    return {"companies_visited": companies_visited}
