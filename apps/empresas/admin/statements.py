from django.contrib import admin
from django.db import models

from apps.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline
from apps.empresas.admin.filters.base import HasQuarterFilter

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

class BaseStatementAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "date",
        "year",
        "period",
        "company",
    ]

    search_fields = [
        "company__ticker",
        "company__name",
    ]

    list_filter = [
        "is_ttm",
        "date",
        "period",
    ]


@admin.register(IncomeStatement)
class IncomeStatementAdmin(BaseStatementAdmin):
    pass


@admin.register(BalanceSheet)
class BalanceSheetAdmin(BaseStatementAdmin):
    pass


@admin.register(CashflowStatement)
class CashflowStatementAdmin(BaseStatementAdmin):
    pass


@admin.register(RentabilityRatio)
class RentabilityRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(LiquidityRatio)
class LiquidityRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(MarginRatio)
class MarginRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(FreeCashFlowRatio)
class FreeCashFlowRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(PerShareValue)
class PerShareValueAdmin(BaseStatementAdmin):
    pass


@admin.register(NonGaap)
class NonGaapAdmin(BaseStatementAdmin):
    pass


@admin.register(OperationRiskRatio)
class OperationRiskRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(EnterpriseValueRatio)
class EnterpriseValueRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(CompanyGrowth)
class CompanyGrowthAdmin(BaseStatementAdmin):
    pass


@admin.register(EficiencyRatio)
class EficiencyRatioAdmin(BaseStatementAdmin):
    pass


@admin.register(PriceToRatio)
class PriceToRatioAdmin(BaseStatementAdmin):
    pass




class HasAverageQuarterFilter(HasQuarterFilter):
    statements = [
        IncomeStatement,
        BalanceSheet,
        CashflowStatement,
    ]


class IncomeStatementInline(BaseJSONWidgetInline):
    model = IncomeStatement
    jazzmin_tab_id = "IncomeStatement"


class BalanceSheetInline(BaseJSONWidgetInline):
    model = BalanceSheet
    jazzmin_tab_id = "BalanceSheet"


class CashflowStatementInline(BaseJSONWidgetInline):
    model = CashflowStatement
    jazzmin_tab_id = "CashflowStatement"


class RentabilityRatioInline(BaseJSONWidgetInline):
    model = RentabilityRatio
    jazzmin_tab_id = "RentabilityRatio"


class LiquidityRatioInline(BaseJSONWidgetInline):
    model = LiquidityRatio
    jazzmin_tab_id = "LiquidityRatio"


class MarginRatioInline(BaseJSONWidgetInline):
    model = MarginRatio
    jazzmin_tab_id = "MarginRatio"


class FreeCashFlowRatioInline(BaseJSONWidgetInline):
    model = FreeCashFlowRatio
    jazzmin_tab_id = "FreeCashFlowRatio"


class PerShareValueInline(BaseJSONWidgetInline):
    model = PerShareValue
    jazzmin_tab_id = "PerShareValue"


class NonGaapInline(BaseJSONWidgetInline):
    model = NonGaap
    jazzmin_tab_id = "NonGaap"


class OperationRiskRatioInline(BaseJSONWidgetInline):
    model = OperationRiskRatio
    jazzmin_tab_id = "OperationRiskRatio"


class EnterpriseValueRatioInline(BaseJSONWidgetInline):
    model = EnterpriseValueRatio
    jazzmin_tab_id = "EnterpriseValueRatio"


class CompanyGrowthInline(BaseJSONWidgetInline):
    model = CompanyGrowth
    jazzmin_tab_id = "CompanyGrowth"


class EficiencyRatioInline(BaseJSONWidgetInline):
    model = EficiencyRatio
    jazzmin_tab_id = "EficiencyRatio"


class PriceToRatioInline(BaseJSONWidgetInline):
    model = PriceToRatio
    jazzmin_tab_id = "PriceToRatio"


@admin.register(CompanyStatementsProxy)
class CompanyStatementsProxyAdmin(BaseCompanyAdmin):
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

    list_filter = []

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
        return CompanyStatementsProxy.objects.prefetch_historical_data().get(id=object_id)
