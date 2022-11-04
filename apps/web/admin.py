from django.contrib import admin

from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailTrack,
    WebsiteLegalPage,
)


@admin.register(WebsiteLegalPage)
class WebsiteLegalPageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
    ]


@admin.register(WebsiteEmailTrack)
class WebsiteEmailTrackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email_related",
        "opened",
        "sent_to",
    ]


@admin.register(WebsiteEmail)
class WebsiteEmailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "opening_rate",
        "campaign",
        "sent",
        "date_to_send",
    ]
    list_editable = [
        "campaign",
        "date_to_send",
    ]
