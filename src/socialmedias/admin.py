from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget
from import_export.admin import ImportExportActionModelAdmin

from .models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    DefaultContent,
    DefaultTilte,
    Emoji,
    Hashtag,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    SocialmediaAuth,
    TermSharedHistorial,
)


@admin.register(SocialmediaAuth)
class SocialmediaAuthAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = ["title", "user", "socialmedia"]


@admin.register(DefaultContent)
class DefaultContentAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "for_content", "purpose"]
    list_editable = ["title", "for_content", "purpose"]


@admin.register(DefaultTilte)
class DefaultTilteAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "title", "for_content", "purpose"]
    list_editable = ["title", "for_content", "purpose"]


@admin.register(Emoji)
class EmojiAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "emoji"]


@admin.register(Hashtag)
class HashtagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "platform",
        "is_trending",
    ]


@admin.register(CompanySharedHistorial)
class CompanySharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "content_shared",
    ]


@admin.register(BlogSharedHistorial)
class BlogSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "content_shared",
    ]


@admin.register(NewsSharedHistorial)
class NewsSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "company_related",
    ]


@admin.register(TermSharedHistorial)
class TermSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "content_shared",
    ]


@admin.register(ProfileSharedHistorial)
class ProfileSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "content_shared",
    ]


@admin.register(QuestionSharedHistorial)
class QuestionSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "date_shared",
        "post_type",
        "platform_shared",
        "social_id",
        "content_shared",
    ]
