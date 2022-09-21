from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.general.models import Period
from apps.empresas.outils.update import UpdateCompany
from apps.empresas.utils import arrange_quarters
from apps.empresas.admin.base import BaseJSONWidgetInline, update_financials
from apps.empresas.models import Company, TopInstitutionalOwnership, CompanyUpdateLog


@admin.register(CompanyUpdateLog)
class CompanyUpdateLogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = [
        "id",
        "company",
        "date",
        "where",
        "had_error",
    ]

    list_filter = [
        "had_error",
    ]


class TopInstitutionalOwnershipInline(BaseJSONWidgetInline):
    model = TopInstitutionalOwnership
    jazzmin_tab_id = "top-institutionals"


class CompanyUpdateLogInline(BaseJSONWidgetInline):
    model = CompanyUpdateLog
    jazzmin_tab_id = "logs"


@admin.action(description="Match quarters")
def match_quarters(modeladmin, request, queryset):
    for query in queryset:
        arrange_quarters(query)


@admin.action(description="Calculate averages")
def calculate_averages(modeladmin, request, queryset):
    for query in queryset:
        for period in Period.objects.all():
            UpdateCompany(query).update_average_financials_statements(period)


@admin.action(description="Calculate ttm")
def calculate_ttm(modeladmin, request, queryset):
    for query in queryset:
        UpdateCompany(query).create_ttm()


@admin.action(description="Calculate ttm and averages")
def calculate_averages_and_ttm(modeladmin, request, queryset):
    for query in queryset:
        UpdateCompany(query).create_ttm()
        for period in Period.objects.all():
            UpdateCompany(query).update_average_financials_statements(period)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    actions = [
        match_quarters,
        update_financials,
        calculate_averages,
        calculate_ttm,
        calculate_averages_and_ttm,
    ]

    inlines = [
        TopInstitutionalOwnershipInline,
        CompanyUpdateLogInline,
    ]

    list_display = [
        "id",
        "name",
        "last_update",
        "no_incs",
        "no_bs",
        "no_cfs",
        "description_translated",
        "has_logo",
        "has_ttm",
    ]

    list_filter = [
        "no_incs",
        "no_bs",
        "no_cfs",
        "updated",
        "description_translated",
        "has_logo",
        "has_error",
        "exchange__main_org",
    ]

    list_editable = [
        "no_incs",
        "no_bs",
        "no_cfs",
        "description_translated",
        "has_logo",
    ]

    search_fields = ["name", "ticker"]

    jazzmin_form_tabs = [
        ("general", "Company"),
        ("top-institutionals", "Top Institutions"),
        ("logs", "Logs"),
    ]
