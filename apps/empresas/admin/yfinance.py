from django.contrib import admin

from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline, BaseStatementAdmin
from apps.empresas.admin.filters.base import HasQuarterFilter

from apps.empresas.models import (
    BalanceSheetYFinance,
    CashflowStatementYFinance,
    IncomeStatementYFinance,
    CompanyYFinanceProxy
)


@admin.register(BalanceSheetYFinance)
class BalanceSheetYFinanceAdmin(BaseStatementAdmin):
    pass


@admin.register(CashflowStatementYFinance)
class CashflowStatementYFinanceAdmin(BaseStatementAdmin):
    pass


@admin.register(IncomeStatementYFinance)
class IncomeStatementYFinanceAdmin(BaseStatementAdmin):
    pass


class HasYFinanceQuarterFilter(HasQuarterFilter):
    statements = [
        IncomeStatementYFinance,
        BalanceSheetYFinance,
        CashflowStatementYFinance,
    ]


class IncomeStatementYFinanceInline(BaseJSONWidgetInline):
    model = IncomeStatementYFinance
    jazzmin_tab_id = "income-statement"


class BalanceSheetYFinanceInline(BaseJSONWidgetInline):
    model = BalanceSheetYFinance
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementYFinanceInline(BaseJSONWidgetInline):
    model = CashflowStatementYFinance
    jazzmin_tab_id = "cashflow-statement"


@admin.register(CompanyYFinanceProxy)
class CompanyYFinanceProxyAdmin(BaseCompanyAdmin):
    inlines = [
        IncomeStatementYFinanceInline,
        BalanceSheetYFinanceInline,
        CashflowStatementYFinanceInline
    ]
    list_filter = BaseCompanyAdmin.list_filter + [
        HasYFinanceQuarterFilter
    ]
