from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget
from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline

from apps.empresas.models import (
    BalanceSheetAsReported,
    IncomeStatementAsReported,
    CashflowStatementAsReported,
    CompanyAsReportedProxy,
)


@admin.register(IncomeStatementAsReported)
class IncomeStatementAsReportedAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = [
        "id",
        "period",
        "company",
    ]

    search_fields = [
        "company__id",
        "company__ticker",
        "company__name",
    ]

    list_filter = [
        "period",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("period", "company")


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
