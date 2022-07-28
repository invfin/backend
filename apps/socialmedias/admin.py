from django.contrib import admin

from .models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    DefaultTilte,
    DefaultContent,
    Emoji,
    Hashtag,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)


@admin.register(DefaultContent)
class DefaultContentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        "for_content",
        "purpose"
    ]



@admin.register(DefaultTilte)
class DefaultTilteAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        "for_content",
        "purpose"
    ]

@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'emoji'
    ]

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'platform',
        'is_trending',
    ]


@admin.register(CompanySharedHistorial)
class CompanySharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'content_shared',
    ]


@admin.register(BlogSharedHistorial)
class BlogSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'content_shared',
    ]


@admin.register(NewsSharedHistorial)
class NewsSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'company_related',
    ]


@admin.register(TermSharedHistorial)
class TermSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'content_shared',
    ]


@admin.register(ProfileSharedHistorial)
class ProfileSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'content_shared',
    ]


@admin.register(QuestionSharedHistorial)
class QuestionSharedHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'date_shared',
        'post_type',
        'platform_shared',
        'social_id',
        'content_shared',
    ]