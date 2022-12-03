from django.contrib.auth import get_user_model
from django.db.models import CASCADE, SET_NULL, BooleanField, CharField, ForeignKey

from src.emailing.abstracts import AbstractTrackEmail
from src.general.abstracts import AbstractGenericModels

from . import constants

User = get_user_model()


class Notification(AbstractGenericModels):
    user = ForeignKey(User, on_delete=CASCADE)
    notification_type = CharField(max_length=500, choices=constants.NOTIFICATIONS_TYPE)
    is_seen = BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        db_table = "notifications"


class EmailNotification(AbstractTrackEmail):
    email_related = ForeignKey(Notification, null=True, blank=True, on_delete=SET_NULL, related_name="email_related")

    class Meta:
        verbose_name = "Email from notifications"
        db_table = "emails_notifications"
