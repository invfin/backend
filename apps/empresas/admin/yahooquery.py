from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.models import (
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
    IncomeStatementYahooQuery,
    KeyStatsYahooQuery,
    CompanyYahooQueryProxy
)

class IncomeStatementYahooQueryInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = IncomeStatementYahooQuery
    extra = 0
    jazzmin_tab_id = "income-statement"


class BalanceSheetYahooQueryInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = BalanceSheetYahooQuery
    extra = 0
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementYahooQueryInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = CashflowStatementYahooQuery
    extra = 0
    jazzmin_tab_id = "cashflow-statement"


class KeyStatsYahooQueryInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = KeyStatsYahooQuery
    extra = 0
    jazzmin_tab_id = "key-stats"


@admin.register(CompanyYahooQueryProxy)
class CompanyYahooQueryProxyAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementYahooQueryInline,
        BalanceSheetYahooQueryInline,
        CashflowStatementYahooQueryInline
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

    list_display = [
        "id",
        "ticker",
        "name",
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
        ("key-stats", "Key Stats"),
    ]
