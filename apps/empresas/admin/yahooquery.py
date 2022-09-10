from django.contrib import admin

from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline
from apps.empresas.admin.filters.base import HasQuarterFilter
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
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


@admin.action(description='Update financials')
def update_financials(modeladmin, request, queryset):
    for query in queryset:
        RetrieveCompanyData(query).create_financials_yahooquery("a")
        RetrieveCompanyData(query).create_financials_yahooquery("q")


@admin.action(description='Update stats')
def update_stats(modeladmin, request, queryset):
    for query in queryset:
        RetrieveCompanyData(query).create_key_stats_yahooquery()


@admin.register(CompanyYahooQueryProxy)
class CompanyYahooQueryProxyAdmin(BaseCompanyAdmin):
    actions = [
        update_financials,
        update_stats,
    ]
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
        "has_inc_quarter",
        "has_bs_quarter",
        "has_cf_quarter",
        "has_key_stats",
    ]

    jazzmin_form_tabs = BaseCompanyAdmin.jazzmin_form_tabs + [
        ("key-stats", "Key Stats"),
    ]

