from django.contrib import admin

from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline

from apps.empresas.models import (
    BalanceSheetAsReported,
    IncomeStatementAsReported,
    CashflowStatementAsReported,
    CompanyAsReportedProxy,
)


class IncomeStatementAsReportedInline(BaseJSONWidgetInline):
    model = IncomeStatementAsReported
    jazzmin_tab_id = "income-statement"


class BalanceSheetAsReportedInline(BaseJSONWidgetInline):
    model = BalanceSheetAsReported
    jazzmin_tab_id = "balance-sheet"


class CashflowStatementAsReportedInline(BaseJSONWidgetInline):
    model = CashflowStatementAsReported
    jazzmin_tab_id = "cashflow-statement"


@admin.register(CompanyAsReportedProxy)
class CompanyAsReportedProxyAdmin(BaseCompanyAdmin):
    inlines = [
        IncomeStatementAsReportedInline,
        BalanceSheetAsReportedInline,
        CashflowStatementAsReportedInline,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(exchange__main_org__name="Estados Unidos")
        return queryset
