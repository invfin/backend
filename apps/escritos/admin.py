from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from import_export.admin import ImportExportActionModelAdmin

from .models import (
    Term,
    TermContent,
    TermCorrection,
    TermsComment,
    TermsRelatedToResume,
)


@admin.action(description='Look for images')
def find_images(modeladmin, request, queryset):
    for query in queryset:
        query.save_secondary_info('term')
        query.save()


@admin.register(TermsRelatedToResume)
class TermsRelatedToResumeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'term_to_keep',
        'term_to_delete'
    ]


class TermContentInline(admin.StackedInline):
    model = TermContent
    extra = 0
    jazzmin_tab_id = "content"


@admin.register(TermContent)
class TermContentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]


@admin.register(Term)
class TermAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [TermContentInline]

    actions = [find_images]

    list_display = [
        "id",
        'term_link',
        "title",
        "slug",
        'category',
        'status',
        'total_votes',
        'total_views',
        'times_shared',
        'published_at',
        'created_at',
        'updated_at',
    ]

    list_editable = [
        "title",
        "slug",
        'category',
        'status',
    ]
    search_fields = [
        'title'
    ]
    jazzmin_form_tabs = [
        ("general", "Company"),
        ("content", "Term parts"),
    ]

    def term_link(self, obj):
        link = reverse(f'web:manage_single_term', args=(obj.slug,))
        return format_html(f'<a target="_blank" href="{link}">{obj.title}</a>')
    term_link.short_description = 'term'


@admin.register(TermCorrection)
class TermCorrectionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]


@admin.register(TermsComment)
class TermsCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at'
    ]
    search_fields = ['author__username']
