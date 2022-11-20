from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget
from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline

from apps.empresas.models import (
    BalanceSheetAsReported,
    IncomeStatementAsReported,
    CashflowStatementAsReported,
    CompanyAsReportedProxy,
    StatementItemConcept,
    StatementItem,
)


@admin.register(StatementItemConcept)
class StatementItemConceptAdmin(admin.ModelAdmin):
    list_display = ["id", "concept", "corresponding_final_item"]


@admin.register(StatementItem)
class StatementItemAdmin(admin.ModelAdmin):
    list_display = ["id", "concept"]

    def get_object(self, request, object_id, from_field=None):
        return StatementItem.objects.select_related("concept", "currency").get(id=object_id)


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

    def get_object(self, request, object_id, from_field=None):
        return (
            IncomeStatementAsReported.objects.select_related("period", "company")
            .prefetch_related("fields", "fields__concept")
            .get(id=object_id)
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("period", "company")
            .prefetch_related("fields", "fields__concept")
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
