from django.urls import path

from .views import (
    PublicNotificationsAPIView,
)

urlpatterns = [
    path("notifications/", PublicNotificationsAPIView.as_view(), name="notifications-api"),
]
