from django.contrib import admin

from apps.empresas.models import (
    BalanceSheetFinprep,
    CashflowStatementFinprep,
    IncomeStatementFinprep,
    CompanyFinprepProxy
)


class IncomeStatementFinprepInline(admin.StackedInline):
    model = IncomeStatementFinprep
    extra = 0
    jazzmin_tab_id = "income-statement"


class BalanceSheetFinprepInline(admin.StackedInline):
    model = BalanceSheetFinprep
    extra = 0
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementFinprepInline(admin.StackedInline):
    model = CashflowStatementFinprep
    extra = 0
    jazzmin_tab_id = "cashflow-statement"


@admin.register(CompanyFinprepProxy)
class CompanyFinprepProxyAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementFinprepInline,
        BalanceSheetFinprepInline,
        CashflowStatementFinprepInline
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
    ]
