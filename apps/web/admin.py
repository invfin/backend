from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailTrack,
    WebsiteLegalPage,
    Roadmap,
    RoadmapComment,
)


class RoadmapCommentInline(admin.StackedInline):
    model = RoadmapComment
    fields = [
        "author",
        "content",
    ]
    extra = 0
    jazzmin_tab_id = "comments"


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    inlines = [RoadmapCommentInline]
    list_display = [
        "title",
        "slug",
        "author",
        "status",
    ]
    list_editable = [
        "status",
    ]
    jazzmin_form_tabs = [
        ("general", "Roadmap"),
        ("comments", "Comments"),
    ]


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
