from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from django_json_widget.widgets import JSONEditorWidget
from import_export.admin import ImportExportActionModelAdmin

from .filters import TermsHasInformationCleanFilter, TermsHasRequestImprovementFilter
from .models import Term, TermContent, TermCorrection, TermsComment, TermsRelatedToResume


@admin.action(description="Look for images")
def find_images(modeladmin, request, queryset):
    for query in queryset:
        query.save_secondary_info("term")
        query.save()


@admin.register(TermsRelatedToResume)
class TermsRelatedToResumeAdmin(admin.ModelAdmin):
    list_display = ["id", "term_to_keep", "term_to_delete"]


class TermContentInline(admin.StackedInline):
    model = TermContent
    extra = 0
    jazzmin_tab_id = "content"


@admin.register(TermContent)
class TermContentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "term_related",
    ]
    list_filter = [
        "term_related",
    ]


@admin.register(Term)
class TermAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    inlines = [TermContentInline]

    actions = [find_images]

    list_display = [
        "id",
        "edit_term",
        "view_term",
        "title",
        "slug",
        "category",
        "status",
        "total_votes",
        "total_views",
        "times_shared",
    ]

    list_editable = [
        "title",
        "slug",
        "category",
        "status",
    ]
    list_filter = [
        "status",
        TermsHasRequestImprovementFilter,
        TermsHasInformationCleanFilter,
    ]
    search_fields = [
        "title",
    ]
    jazzmin_form_tabs = [
        ("general", "Term"),
        ("content", "Term parts"),
    ]

    def edit_term(self, obj):
        link = reverse("web:manage_single_term", args=(obj.slug,))
        return format_html(f'<a target="_blank" href="{link}">{obj.title}</a>')

    edit_term.short_description = "Edit term"

    def view_term(self, obj):
        link = obj.get_absolute_url()
        return format_html(f'<a target="_blank" href="{link}">{obj.title}</a>')

    view_term.short_description = "View term"


@admin.register(TermCorrection)
class TermCorrectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(TermsComment)
class TermsCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "created_at"]
    search_fields = ["author__username"]
