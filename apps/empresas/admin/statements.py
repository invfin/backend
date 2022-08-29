from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.models import (
    CompanyStatementsProxy,
    IncomeStatement,
    BalanceSheet,
    CashflowStatement,
    RentabilityRatio,
    LiquidityRatio,
    MarginRatio,
    FreeCashFlowRatio,
    PerShareValue,
    NonGaap,
    OperationRiskRatio,
    EnterpriseValueRatio,
    CompanyGrowth,
    EficiencyRatio,
    PriceToRatio,
)


class IncomeStatementInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = IncomeStatement
    jazzmin_tab_id = "IncomeStatement"


class BalanceSheetInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = BalanceSheet
    jazzmin_tab_id = "BalanceSheet"


class CashflowStatementInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = CashflowStatement
    jazzmin_tab_id = "CashflowStatement"


class RentabilityRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = RentabilityRatio
    jazzmin_tab_id = "RentabilityRatio"


class LiquidityRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = LiquidityRatio
    jazzmin_tab_id = "LiquidityRatio"


class MarginRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = MarginRatio
    jazzmin_tab_id = "MarginRatio"


class FreeCashFlowRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = FreeCashFlowRatio
    jazzmin_tab_id = "FreeCashFlowRatio"


class PerShareValueInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = PerShareValue
    jazzmin_tab_id = "PerShareValue"


class NonGaapInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = NonGaap
    jazzmin_tab_id = "NonGaap"


class OperationRiskRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = OperationRiskRatio
    jazzmin_tab_id = "OperationRiskRatio"


class EnterpriseValueRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = EnterpriseValueRatio
    jazzmin_tab_id = "EnterpriseValueRatio"


class CompanyGrowthInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = CompanyGrowth
    jazzmin_tab_id = "CompanyGrowth"


class EficiencyRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = EficiencyRatio
    jazzmin_tab_id = "EficiencyRatio"


class PriceToRatioInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    model = PriceToRatio
    jazzmin_tab_id = "PriceToRatio"


@admin.register(CompanyStatementsProxy)
class CompanyStatementsProxyAdmin(admin.ModelAdmin):
    inlines = [
        IncomeStatementInline,
        BalanceSheetInline,
        CashflowStatementInline,
        RentabilityRatioInline,
        LiquidityRatioInline,
        MarginRatioInline,
        FreeCashFlowRatioInline,
        PerShareValueInline,
        NonGaapInline,
        OperationRiskRatioInline,
        EnterpriseValueRatioInline,
        CompanyGrowthInline,
        EficiencyRatioInline,
        PriceToRatioInline,
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
        ("IncomeStatement", "Income Statement"),
        ("BalanceSheet", "Balance Sheet"),
        ("CashflowStatement", "Cashflow Statement"),
        ("RentabilityRatio", "Rentability Ratio"),
        ("LiquidityRatio", "Liquidity Ratio"),
        ("MarginRatio", "Margin Ratio"),
        ("FreeCashFlowRatio", "FreeCashFlow Ratio"),
        ("PerShareValue", "PerShare Value"),
        ("NonGaap", "Non Gaap"),
        ("OperationRiskRatio", "Operation Risk Ratio"),
        ("EnterpriseValueRatio", "Enterprise Value Ratio"),
        ("CompanyGrowth", "Company Growth"),
        ("EficiencyRatio", "Eficiency Ratio"),
        ("PriceToRatio", "Price To Ratio"),
    ]

    def get_object(self, request, object_id: str, from_field):
        return Company.objects.prefetch_historical_data().get(id=object_id)
