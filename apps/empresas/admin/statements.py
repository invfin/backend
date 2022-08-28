from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.models import (
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

