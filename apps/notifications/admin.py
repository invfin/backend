from django.contrib import admin

from .models import EmailNotification, Notification



@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "email_related"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "object",
        "notification_type",
        "is_seen",
        "content_type",
        "object_id",
        "date",
    ]
