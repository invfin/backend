from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Currency, ExchangeRate, UserDefaultCurrency


@admin.register(UserDefaultCurrency)
class UserDefaultCurrencyAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["pk", "user", "currency"]


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["pk", "base", "target", "conversion_rate"]


@admin.register(Currency)
class CurrencyAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "currency",
        "symbol",
        "name",
        "spanish_name",
        "code",
        "iso",
        "decimals",
    ]
    list_editable = [
        "symbol",
        "name",
        "spanish_name",
        "code",
        "iso",
        "decimals",
    ]
