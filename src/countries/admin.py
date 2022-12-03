from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Country


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
