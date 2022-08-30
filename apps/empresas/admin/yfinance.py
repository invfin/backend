from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.models import (
    BalanceSheetYFinance,
    CashflowStatementYFinance,
    IncomeStatementYFinance,
    CompanyYFinanceProxy
)


class IncomeStatementYFinanceInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = IncomeStatementYFinance
    extra = 0
    jazzmin_tab_id = "income-statement"


class BalanceSheetYFinanceInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = BalanceSheetYFinance
    extra = 0
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementYFinanceInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = CashflowStatementYFinance
    extra = 0
    jazzmin_tab_id = "cashflow-statement"


@admin.register(CompanyYFinanceProxy)
class CompanyYFinanceProxyAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementYFinanceInline,
        BalanceSheetYFinanceInline,
        CashflowStatementYFinanceInline
    ]
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
    ]
