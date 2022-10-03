from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.parse.yahoo_query import YahooQueryInfo
from apps.empresas.utils import arrange_quarters
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
from apps.empresas.admin.filters.base import (
    NewCompanyToParseFilter,
    HasQuarterFilter,
)


class BaseJSONWidgetInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    extra = 0


class BaseStatementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = [
        "id",
        "date",
        "year",
        "period",
        "company",
    ]

    search_fields = [
        "company__id",
        "company__ticker",
        "company__name",
    ]

    list_filter = [
        "company__exchange__main_org",
        "company__exchange",
        "date",
        "period",
    ]


@admin.action(description="Update financials")
def update_financials(modeladmin, request, queryset):
    for query in queryset:
        RetrieveCompanyData(query).create_financials_yahooquery("a")
        RetrieveCompanyData(query).create_financials_yahooquery("q")
        RetrieveCompanyData(query).create_financials_yfinance("a")
        RetrieveCompanyData(query).create_financials_yfinance("q")
        arrange_quarters(query)


class BaseCompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    actions = [
        update_financials,
    ]

    fieldsets = (
        (
            "Company",
            {
                "classes": ("jazzmin-tab-general",),
                "fields": [
                    "ticker",
                    "name",
                ],
            },
        ),
    )

    list_filter = [
        NewCompanyToParseFilter,
    ]

    list_display = [
        "id",
        "ticker",
        "name",
        "has_inc",
        "has_bs",
        "has_cf",
    ]

    search_fields = [
        "id",
        "ticker",
        "name",
    ]

    jazzmin_form_tabs = [
        ("general", "Company"),
        ("income-statement", "Income Statement"),
        ("balance-sheet", "Balance Sheet"),
        ("cashflow-statement", "Cashflow Statement"),
    ]
