from django.contrib import admin

from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline
from apps.empresas.admin.filters.base import HasQuarterFilter
from apps.empresas.models import (
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
    IncomeStatementYahooQuery,
    KeyStatsYahooQuery,
    CompanyYahooQueryProxy
)


class HasYahooQueryQuarterFilter(HasQuarterFilter):
    statements = [
        IncomeStatementYahooQuery,
        BalanceSheetYahooQuery,
        CashflowStatementYahooQuery,
    ]


class IncomeStatementYahooQueryInline(BaseJSONWidgetInline):
    model = IncomeStatementYahooQuery
    jazzmin_tab_id = "income-statement"


class BalanceSheetYahooQueryInline(BaseJSONWidgetInline):
    model = BalanceSheetYahooQuery
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementYahooQueryInline(BaseJSONWidgetInline):
    model = CashflowStatementYahooQuery
    jazzmin_tab_id = "cashflow-statement"


class KeyStatsYahooQueryInline(BaseJSONWidgetInline):
    model = KeyStatsYahooQuery
    jazzmin_tab_id = "key-stats"


@admin.register(CompanyYahooQueryProxy)
class CompanyYahooQueryProxyAdmin(BaseCompanyAdmin):
    inlines = [
        IncomeStatementYahooQueryInline,
        BalanceSheetYahooQueryInline,
        CashflowStatementYahooQueryInline,
        KeyStatsYahooQueryInline
    ]

    list_filter = BaseCompanyAdmin.list_filter + [
        HasYahooQueryQuarterFilter
    ]

    list_display = BaseCompanyAdmin.list_display + [
        "has_key_stats",
    ]

    jazzmin_form_tabs = BaseCompanyAdmin.jazzmin_form_tabs + [
        ("key-stats", "Key Stats"),
    ]

