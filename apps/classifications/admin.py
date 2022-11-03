from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Category, Tag


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Tag)
class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]
