from django.contrib import admin

from apps.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    Company,
    CompanyGrowth,
    CompanyStockPrice,
    CompanyUpdateLog,
    EficiencyRatio,
    EnterpriseValueRatio,
    FreeCashFlowRatio,
    IncomeStatement,
    InstitutionalOrganization,
    LiquidityRatio,
    MarginRatio,
    NonGaap,
    OperationRiskRatio,
    PerShareValue,
    PriceToRatio,
    RentabilityRatio,
    TopInstitutionalOwnership,
)


@admin.register(CompanyUpdateLog)
class CompanyUpdateLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date',
        'where',
        'had_error',
        'error_message'
    ]
    search_fields = ['company__name']


@admin.register(InstitutionalOrganization)
class InstitutionalOrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    search_fields = ['name']


@admin.register(TopInstitutionalOwnership)
class TopInstitutionalOwnershipAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'year',
        'company',
        'organization',
        'percentage_held',
        'position',
        'value',
    ]



class CashflowStatementAdmin(admin.TabularInline):
    model = CashflowStatement
    jazzmin_tab_id = "cf"

class IncomeStatementAdmin(admin.TabularInline):
    model = IncomeStatement
    jazzmin_tab_id = "in"

class BalanceSheetAdmin(admin.TabularInline):
    model = BalanceSheet
    jazzmin_tab_id = "bs"



# @admin.register(IncomeStatement)
# class IncomeStatementAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'company',
#         'date'
#     ]
#     search_fields = ['company_name', 'company_ticker']


# @admin.register(BalanceSheet)
# class BalanceSheetAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'company',
#         'date'
#     ]
#     search_fields = ['company_name', 'company_ticker']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        CashflowStatementAdmin,
IncomeStatementAdmin,
BalanceSheetAdmin,
    ]
    jazzmin_form_tabs = [
        ("general", "Info"),
        ("bs", "Profile"),
        ("in", "Writter"),
        ("cf", "Meta"),
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




@admin.register(CompanyGrowth)
class CompanyGrowthAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(EficiencyRatio)
class EficiencyRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(EnterpriseValueRatio)
class EnterpriseValueRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']





@admin.register(RentabilityRatio)
class RentabilityRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(MarginRatio)
class MarginRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(PriceToRatio)
class PriceToRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(LiquidityRatio)
class LiquidityRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(OperationRiskRatio)
class OperationRiskRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(FreeCashFlowRatio)
class FreeCashFlowRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(PerShareValue)
class PerShareValueAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(CompanyStockPrice)
class CompanyStockPriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company_related',
        'date'
    ]
    search_fields = ['company_related_name']


@admin.register(NonGaap)
class NonGaapAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']

