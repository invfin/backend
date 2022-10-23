from django.contrib import admin

from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailsType,
    WebsiteEmailTrack,
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign,
    UsersCategory,
)


@admin.register(UsersCategory)
class UsersCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
        "name_for_user",
        "show_to_user",
    ]
    list_editable = [
        "name_for_user",
        "show_to_user",
    ]
    filter_horizontal = [
        "email_type_related",
        "users",
    ]


@admin.register(PromotionCampaign)
class PromotionCampaignAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
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
        "web_promotion_type",
        "web_location",
        "social_media",
        "publication_date",
        "campaign_related",
        "reuse",
        "times_to_reuse",
        "clicks_by_user",
        "clicks_by_not_user",
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
        "type_related",
        "sent",
        "date_to_send",
    ]
    list_editable = [
        "type_related",
        "date_to_send",
    ]


@admin.register(WebsiteEmailsType)
class WebsiteEmailsTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
