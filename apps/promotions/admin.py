from django.contrib import admin

from .models import (
    Promotion,
    Campaign,
)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
        "focused_on",
        "start_date",
        "end_date",
    ]
    filter_horizontal = [
        "categories",
        "tags",
    ]
    list_editable = [
        "focused_on",
        "start_date",
        "end_date",
    ]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
        "prize",
        "has_prize",
        "shareable_url",
        "redirect_to",
        "medium",
        "web_promotion_style",
        "web_location",
        "social_media",
        "publication_date",
        "campaign",
        "reuse",
        "times_to_reuse",
        "clicks_by_user",
        "clicks_by_not_user",
    ]
