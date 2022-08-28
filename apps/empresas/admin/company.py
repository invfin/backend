from django.contrib import admin

from .statements import (
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
)

from apps.empresas.models import (
    Company
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
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

    list_display = [
        'id',
        'name',
        'last_update',
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]

    list_filter = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'updated',
        'description_translated',
        'has_logo',
        'has_error',
        'exchange__main_org'
    ]

    list_editable = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]

    search_fields = ['name', 'ticker']

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
