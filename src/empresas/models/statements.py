from django.db.models import (
    SET_NULL,
    BooleanField,
    DateField,
    ForeignKey,
    IntegerField,
    Model,
)

from src.empresas.managers import BaseStatementManager
from src.empresas.models import Company
from src.empresas.querysets.statements import BaseStatementQuerySet, StatementQuerySet
from src.general.mixins import BaseToAllMixin
from src.periods.models import Period
from src.empresas.fields import EntryStatementField


class BaseStatement(Model, BaseToAllMixin):
    date = IntegerField(default=0)
    year = DateField(null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    period = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    reported_currency = ForeignKey(
        "currencies.Currency",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    objects = BaseStatementManager.from_queryset(BaseStatementQuerySet)()

    class Meta:
        abstract = True
        get_latest_by = ["-date", "period"]
        ordering = ["-date", "period"]
        base_manager_name = "objects"

    def __str__(self) -> str:
        period = self.period or self.date
        return f"{self.company} - {period}"

    def save(self, *args, **kwargs) -> None:
        self.set_date()
        super().save(*args, **kwargs)

    def set_date(self) -> None:
        if self.date == 0:
            if not self.year and self.period:
                self.date = self.period.year
            elif self.year:
                self.date = self.year.year


class BaseFinalStatement(BaseStatement):
    is_ttm = BooleanField(default=False)
    from_average = BooleanField(default=False)
    objects = BaseStatementManager.from_queryset(StatementQuerySet)()  # type: ignore

    class Meta:
        abstract = True

    def __str__(self) -> str:
        period = self.period or self.date
        return f"{self.company} - TTM" if self.is_ttm else f"{self.company} - {period}"

    @property
    def date_year(self) -> str:
        return "TTM" if self.is_ttm else f"{self.date}"


class IncomeStatement(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="inc_statements",
    )
    revenue = EntryStatementField()
    cost_of_revenue = EntryStatementField()
    gross_profit = EntryStatementField()
    rd_expenses = EntryStatementField()
    general_administrative_expenses = EntryStatementField()
    selling_marketing_expenses = EntryStatementField()
    sga_expenses = EntryStatementField()
    other_expenses = EntryStatementField()
    operating_expenses = EntryStatementField()
    cost_and_expenses = EntryStatementField()
    interest_expense = EntryStatementField()
    depreciation_amortization = EntryStatementField()
    ebitda = EntryStatementField()
    operating_income = EntryStatementField()
    net_total_other_income_expenses = EntryStatementField()
    income_before_tax = EntryStatementField()
    income_tax_expenses = EntryStatementField()
    net_income = EntryStatementField()
    weighted_average_shares_outstanding = EntryStatementField()
    weighted_average_diluated_shares_outstanding = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Income Statement"
        verbose_name_plural = "Income Statements"
        db_table = "assets_companies_income_statements"


class BalanceSheet(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="balance_sheets",
    )
    cash_and_cash_equivalents = EntryStatementField()
    short_term_investments = EntryStatementField()
    cash_and_short_term_investments = EntryStatementField()
    net_receivables = EntryStatementField()
    inventory = EntryStatementField()
    other_current_assets = EntryStatementField()
    total_current_assets = EntryStatementField()
    property_plant_equipment = EntryStatementField()
    goodwill = EntryStatementField()
    intangible_assets = EntryStatementField()
    goodwill_and_intangible_assets = EntryStatementField()
    long_term_investments = EntryStatementField()
    tax_assets = EntryStatementField()
    other_non_current_assets = EntryStatementField()
    total_non_current_assets = EntryStatementField()
    other_assets = EntryStatementField()
    total_assets = EntryStatementField()
    accounts_payable = EntryStatementField()
    short_term_debt = EntryStatementField()
    tax_payables = EntryStatementField()
    deferred_revenue = EntryStatementField()
    other_current_liabilities = EntryStatementField()
    total_current_liabilities = EntryStatementField()
    long_term_debt = EntryStatementField()
    deferred_revenue_non_current = EntryStatementField()
    deferred_tax_liabilities_non_current = EntryStatementField()
    other_non_current_liabilities = EntryStatementField()
    total_non_current_liabilities = EntryStatementField()
    other_liabilities = EntryStatementField()
    total_liabilities = EntryStatementField()
    common_stocks = EntryStatementField()
    preferred_stocks = EntryStatementField()
    retained_earnings = EntryStatementField()
    accumulated_other_comprehensive_income_loss = EntryStatementField()
    othertotal_stockholders_equity = EntryStatementField()
    total_stockholders_equity = EntryStatementField()
    total_liabilities_and_total_equity = EntryStatementField()
    total_investments = EntryStatementField()
    total_debt = EntryStatementField()
    net_debt = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Balance Sheet"
        verbose_name_plural = "Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements"


class CashflowStatement(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="cf_statements",
    )
    net_income = EntryStatementField()
    depreciation_amortization = EntryStatementField()
    deferred_income_tax = EntryStatementField()
    stock_based_compensation = EntryStatementField()
    change_in_working_capital = EntryStatementField()
    accounts_receivable = EntryStatementField()
    inventory = EntryStatementField()
    accounts_payable = EntryStatementField()
    other_working_capital = EntryStatementField()
    other_non_cash_items = EntryStatementField()
    operating_activities_cf = EntryStatementField()
    investments_property_plant_equipment = EntryStatementField()
    acquisitions_net = EntryStatementField()
    purchases_investments = EntryStatementField()
    sales_maturities_investments = EntryStatementField()
    other_investing_activites = EntryStatementField()
    investing_activities_cf = EntryStatementField()
    debt_repayment = EntryStatementField()
    common_stock_issued = EntryStatementField()
    common_stock_repurchased = EntryStatementField()
    dividends_paid = EntryStatementField()
    other_financing_activities = EntryStatementField()
    financing_activities_cf = EntryStatementField()
    effect_forex_exchange = EntryStatementField()
    net_change_cash = EntryStatementField()
    cash_end_period = EntryStatementField()
    cash_beginning_period = EntryStatementField()
    operating_cf = EntryStatementField()
    capex = EntryStatementField()
    fcf = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Cash flow Statement"
        verbose_name_plural = "Cash flow Statements"
        db_table = "assets_companies_cashflow_statements"

    @property
    def cash_conversion_ratio_to_save(self):
        try:
            return self.fcf / self.net_income
        except Exception:
            return 0


class RentabilityRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="rentability_ratios",
    )
    roa = EntryStatementField()
    roe = EntryStatementField()
    roc = EntryStatementField()
    roce = EntryStatementField()
    rota = EntryStatementField()
    roic = EntryStatementField()
    nopat_roic = EntryStatementField()
    rogic = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Rentability Ratio"
        verbose_name_plural = "Rentability Ratios"
        db_table = "assets_companies_rentability_ratios"


class LiquidityRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="liquidity_ratios",
    )
    cash_ratio = EntryStatementField()
    current_ratio = EntryStatementField()
    quick_ratio = EntryStatementField()
    operating_cashflow_ratio = EntryStatementField()
    debt_to_equity = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Liquidity Ratio"
        verbose_name_plural = "Liquidity Ratios"
        db_table = "assets_companies_liquidity_ratios"


class MarginRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="margins",
    )
    gross_margin = EntryStatementField()
    ebitda_margin = EntryStatementField()
    net_income_margin = EntryStatementField()
    fcf_margin = EntryStatementField()
    fcf_equity_to_net_income = EntryStatementField()
    unlevered_fcf_to_net_income = EntryStatementField()
    unlevered_fcf_ebit_to_net_income = EntryStatementField()
    owners_earnings_to_net_income = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Margin Ratio"
        verbose_name_plural = "Margin Ratios"
        db_table = "assets_companies_margins_ratios"


class FreeCashFlowRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="fcf_ratios",
    )
    fcf_equity = EntryStatementField()
    unlevered_fcf = EntryStatementField()
    unlevered_fcf_ebit = EntryStatementField()
    owners_earnings = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Free cash flow Ratio"
        verbose_name_plural = "Free cash flow Ratios"
        db_table = "assets_companies_freecashflow_ratios"


class PerShareValue(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="per_share_values",
    )
    sales_ps = EntryStatementField()
    book_ps = EntryStatementField()
    tangible_ps = EntryStatementField()
    fcf_ps = EntryStatementField()
    eps = EntryStatementField()
    cash_ps = EntryStatementField()
    operating_cf_ps = EntryStatementField()
    capex_ps = EntryStatementField()
    total_assets_ps = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Per share"
        verbose_name_plural = "Per shares"
        db_table = "assets_companies_per_share_value"


class NonGaap(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="non_gaap_figures",
    )
    normalized_income = EntryStatementField()
    effective_tax_rate = EntryStatementField()
    nopat = EntryStatementField()
    net_working_cap = EntryStatementField()
    average_inventory = EntryStatementField()
    average_accounts_payable = EntryStatementField()
    dividend_yield = EntryStatementField()
    earnings_yield = EntryStatementField()
    fcf_yield = EntryStatementField()
    income_quality = EntryStatementField()
    invested_capital = EntryStatementField()
    market_cap = EntryStatementField()
    net_current_asset_value = EntryStatementField()
    payout_ratio = EntryStatementField()
    tangible_assets = EntryStatementField()
    retention_ratio = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Non GAAP figure"
        verbose_name_plural = "Non GAAP figures"
        db_table = "assets_companies_non_gaap"


class OperationRiskRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="operation_risks_ratios",
    )
    asset_coverage_ratio = EntryStatementField()
    cash_flow_coverage_ratios = EntryStatementField()
    cash_coverage = EntryStatementField()
    debt_service_coverage = EntryStatementField()
    interest_coverage = EntryStatementField()
    operating_cashflow_ratio = EntryStatementField()
    debt_ratio = EntryStatementField()
    long_term_debt_to_capitalization = EntryStatementField()
    total_debt_to_capitalization = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Operation Risk Ratio"
        verbose_name_plural = "Operation Risk Ratios"
        db_table = "assets_companies_operations_risk_ratio"


class EnterpriseValueRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="ev_ratios"
    )
    market_cap = EntryStatementField()
    enterprise_value = EntryStatementField()
    ev_fcf = EntryStatementField()
    ev_operating_cf = EntryStatementField()
    ev_sales = EntryStatementField()
    company_equity_multiplier = EntryStatementField()
    ev_multiple = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Enterprise Value"
        verbose_name_plural = "Enterprise Values"
        db_table = "assets_companies_enterprise_value_ratios"


class CompanyGrowth(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="growth_rates"
    )
    revenue_growth = EntryStatementField()
    cost_revenue_growth = EntryStatementField()
    operating_expenses_growth = EntryStatementField()
    net_income_growth = EntryStatementField()
    shares_buyback = EntryStatementField()
    eps_growth = EntryStatementField()
    fcf_growth = EntryStatementField()
    owners_earnings_growth = EntryStatementField()
    capex_growth = EntryStatementField()
    rd_expenses_growth = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Company growth"
        verbose_name_plural = "Companies growth"
        db_table = "assets_companies_growths"


class EficiencyRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="efficiency_ratios"
    )
    asset_turnover = EntryStatementField()
    inventory_turnover = EntryStatementField()
    fixed_asset_turnover = EntryStatementField()
    accounts_payable_turnover = EntryStatementField()
    cash_conversion_cycle = EntryStatementField()
    days_inventory_outstanding = EntryStatementField()
    days_payables_outstanding = EntryStatementField()
    days_sales_outstanding = EntryStatementField()
    free_cashflow_to_operating_cashflow = EntryStatementField()
    operating_cycle = EntryStatementField()
    cash_conversion_ratio = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Efficiency Ratio"
        verbose_name_plural = "Efficiency Ratios"
        db_table = "assets_companies_eficiency_ratios"


class PriceToRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="price_to_ratios"
    )
    price_book = EntryStatementField()
    price_cf = EntryStatementField()
    price_earnings = EntryStatementField()
    price_earnings_growth = EntryStatementField()
    price_sales = EntryStatementField()
    price_total_assets = EntryStatementField()
    price_fcf = EntryStatementField()
    price_operating_cf = EntryStatementField()
    price_tangible_assets = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Price to Ratio"
        verbose_name_plural = "Price to Ratios"
        db_table = "assets_companies_price_to_ratios"
