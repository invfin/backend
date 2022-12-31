from django.contrib import admin

from import_export.admin import ExportActionModelAdmin

from src.empresas.admin.base import BaseCompanyAdmin, BaseJSONWidgetInline, BaseStatementAdmin
from src.empresas.admin.filters.base import HasQuarterFilter
from src.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    CompanyGrowth,
    CompanyStatementsProxy,
    EficiencyRatio,
    EnterpriseValueRatio,
    FreeCashFlowRatio,
    IncomeStatement,
    LiquidityRatio,
    MarginRatio,
    NonGaap,
    OperationRiskRatio,
    PerShareValue,
    PriceToRatio,
    RentabilityRatio,
)


class BaseFinalAdmin(BaseStatementAdmin):
    list_display = BaseStatementAdmin.list_display + [
        "is_ttm",
        "from_average",
    ]
    list_filter = BaseStatementAdmin.list_filter + [
        "is_ttm",
        "from_average",
    ]


@admin.register(IncomeStatement)
class IncomeStatementAdmin(ExportActionModelAdmin, BaseFinalAdmin):
    pass


@admin.register(BalanceSheet)
class BalanceSheetAdmin(ExportActionModelAdmin, BaseFinalAdmin):
    pass


@admin.register(CashflowStatement)
class CashflowStatementAdmin(ExportActionModelAdmin, BaseFinalAdmin):
    pass


@admin.register(RentabilityRatio)
class RentabilityRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(LiquidityRatio)
class LiquidityRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(MarginRatio)
class MarginRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(FreeCashFlowRatio)
class FreeCashFlowRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(PerShareValue)
class PerShareValueAdmin(BaseFinalAdmin):
    pass


@admin.register(NonGaap)
class NonGaapAdmin(BaseFinalAdmin):
    pass


@admin.register(OperationRiskRatio)
class OperationRiskRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(EnterpriseValueRatio)
class EnterpriseValueRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(CompanyGrowth)
class CompanyGrowthAdmin(BaseFinalAdmin):
    pass


@admin.register(EficiencyRatio)
class EficiencyRatioAdmin(BaseFinalAdmin):
    pass


@admin.register(PriceToRatio)
class PriceToRatioAdmin(BaseFinalAdmin):
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
