from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.parse.yahoo_query import YahooQueryInfo
from apps.empresas.utils import arrange_quarters
from apps.empresas.admin.base import BaseJSONWidgetInline, update_financials
from apps.empresas.models import (
    Company,
    TopInstitutionalOwnership,
    CompanyUpdateLog
)


class TopInstitutionalOwnershipInline(BaseJSONWidgetInline):
    model = TopInstitutionalOwnership
    jazzmin_tab_id = "top-institutionals"


class CompanyUpdateLogInline(BaseJSONWidgetInline):
    model = CompanyUpdateLog
    jazzmin_tab_id = "logs"


@admin.action(description='Match quarters')
def match_quarters(modeladmin, request, queryset):
    for query in queryset:
        YahooQueryInfo(query).match_quarters_with_earning_history_yahooquery()
        arrange_quarters(query)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    actions = [
        match_quarters,
        update_financials,
    ]

    inlines = [
        TopInstitutionalOwnershipInline,
        CompanyUpdateLogInline,
    ]

    list_display = [
        'id',
        'name',
        'last_update',
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]

    list_filter = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'updated',
        'description_translated',
        'has_logo',
        'has_error',
        'exchange__main_org'
    ]

    list_editable = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]

    search_fields = ['name', 'ticker']

    jazzmin_form_tabs = [
        ("general", "Company"),
        ("top-institutionals", "Top Institutions"),
        ("logs", "Logs"),
    ]
