from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Category, Country, Currency, EmailNotification, Industry, Notification, Sector, Tag, Period


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


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Tag)
class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Industry)
class IndustryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "industry"]


@admin.register(Sector)
class SectorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "sector"]


@admin.register(Currency)
class CurrencyAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "currency",
        "symbol",
        "name",
        "spanish_name",
        "accronym",
        "iso",
        "decimals",
    ]
    list_editable = [
        "symbol",
        "name",
        "spanish_name",
        "accronym",
        "iso",
        "decimals",
    ]


@admin.register(Country)
class CountryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "country",
        "name",
        "spanish_name",
        "iso",
        "alpha_2_code",
        "alpha_3_code",
    ]
    list_editable = [
        "name",
        "spanish_name",
        "iso",
        "alpha_2_code",
        "alpha_3_code",
    ]


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "year",
        "period",
    ]
