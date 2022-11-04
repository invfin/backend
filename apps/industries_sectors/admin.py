from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Industry, Sector


@admin.register(Industry)
class IndustryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "industry"]


@admin.register(Sector)
class SectorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "sector"]
