from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    CompanyRequestAPI,
    Endpoint,
    EndpointsCategory,
    Key,
    ReasonKeyRequested,
    SuperinvestorRequestAPI,
    TermRequestAPI,
)


@admin.register(ReasonKeyRequested)
class ReasonKeyRequestedAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    ordering = ['-created']
    search_fields = ['user_username']


class BaseRequestAPIAdmin(admin.ModelAdmin):
    list_display = ['user', 'search', 'path', 'date']
    ordering = ['-date']
    search_fields = ['user_username']


@admin.register(CompanyRequestAPI)
class CompanyRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


@admin.register(TermRequestAPI)
class TermRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


@admin.register(SuperinvestorRequestAPI)
class SuperinvestorRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


class BaseInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0


class CompanyRequestAPIInline(BaseInline):
    jazzmin_tab_id = "companies"
    model = CompanyRequestAPI


class TermRequestAPIInline(BaseInline):
    jazzmin_tab_id = "terms"
    model = TermRequestAPI


class SuperinvestorRequestAPIInline(BaseInline):
    jazzmin_tab_id = "superinvesotrs"
    model = SuperinvestorRequestAPI


class EndpointInline(BaseInline):
    model = Endpoint
    jazzmin_tab_id = "endpoints"


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    # inlines = [
    #     CompanyRequestAPIInline,
    #     TermRequestAPIInline,
    #     SuperinvestorRequestAPIInline,
    # ]
    list_display = ['key', 'user_link', 'created']
    ordering = ['-created']
    search_fields = ['user_username']

    jazzmin_form_tabs = [
        ("general", "User"),
        ("companies", "Companies"),
        ("terms", "Terms"),
        ("superinvesotrs", "Superinvestors"),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "companyrequestapi_set",
            "termrequestapi_set",
            "superinvestorrequestapi_set",
        )

    def user_link(self, obj):
        field = getattr(obj, 'user')
        object_name = field.object_name.lower()
        app_name = field.app_label
        args = field.id
        link = reverse(f'admin:{app_name}_{object_name}_change', args=(args,))
        return format_html(f'<a target="_blank" href="{link}">{field}</a>')
    user_link.short_description = 'user'


@admin.register(EndpointsCategory)
class EndpointsCategoryAdmin(admin.ModelAdmin):
    inlines = [EndpointInline]
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    list_display = ['id', 'title', 'order', 'icon']
    list_editable = list_display[1:]
    jazzmin_form_tabs = [
        ("general", "Main category"),
        ("endpoints", "Endpoints"),
    ]


@admin.register(Endpoint)
class EndpointAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    list_display = [
        'title',
        'title_related',
        'order',
        'url_example',
        'is_premium',
        'is_available',
        'is_deprecated',
        'version',
        'price',
    ]
    list_editable = list_display[1:]
