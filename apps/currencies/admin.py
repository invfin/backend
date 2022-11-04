from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Currency


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
