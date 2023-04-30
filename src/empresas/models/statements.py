from django.db.models import (
    SET_NULL,
    BooleanField,
    DateField,
    FloatField,
    ForeignKey,
    IntegerField,
    Model,
)

from src.empresas.managers import BaseStatementManager
from src.empresas.models import Company
from src.empresas.querysets.statements import BaseStatementQuerySet, StatementQuerySet
from src.general.mixins import BaseToAllMixin
from src.periods.models import Period


class BaseStatement(Model, BaseToAllMixin):
    date = IntegerField(default=0)
    year = DateField(null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    period = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    reported_currency = ForeignKey(
        "currencies.Currency", on_delete=SET_NULL, null=True, blank=True
    )
    objects = BaseStatementManager.from_queryset(BaseStatementQuerySet)()  # type: ignore

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
    def date_year(self):
        return "TTM" if self.is_ttm else f"{self.date}"


class IncomeStatement(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="inc_statements",
    )
    revenue = FloatField(default=0, blank=True, null=True)
    cost_of_revenue = FloatField(default=0, blank=True, null=True)
    gross_profit = FloatField(default=0, blank=True, null=True)
    rd_expenses = FloatField(default=0, blank=True, null=True)
    general_administrative_expenses = FloatField(default=0, blank=True, null=True)
    selling_marketing_expenses = FloatField(default=0, blank=True, null=True)
    sga_expenses = FloatField(default=0, blank=True, null=True)
    other_expenses = FloatField(default=0, blank=True, null=True)
    operating_expenses = FloatField(default=0, blank=True, null=True)
    cost_and_expenses = FloatField(default=0, blank=True, null=True)
    interest_expense = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    ebitda = FloatField(default=0, blank=True, null=True)
    operating_income = FloatField(default=0, blank=True, null=True)
    net_total_other_income_expenses = FloatField(default=0, blank=True, null=True)
    income_before_tax = FloatField(default=0, blank=True, null=True)
    income_tax_expenses = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    weighted_average_shares_outstanding = FloatField(default=0, blank=True, null=True)
    weighted_average_diluated_shares_outstanding = FloatField(default=0, blank=True, null=True)

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
    cash_and_cash_equivalents = FloatField(default=0, blank=True, null=True)
    short_term_investments = FloatField(default=0, blank=True, null=True)
    cash_and_short_term_investments = FloatField(default=0, blank=True, null=True)
    net_receivables = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    other_current_assets = FloatField(default=0, blank=True, null=True)
    total_current_assets = FloatField(default=0, blank=True, null=True)
    property_plant_equipment = FloatField(default=0, blank=True, null=True)
    goodwill = FloatField(default=0, blank=True, null=True)
    intangible_assets = FloatField(default=0, blank=True, null=True)
    goodwill_and_intangible_assets = FloatField(default=0, blank=True, null=True)
    long_term_investments = FloatField(default=0, blank=True, null=True)
    tax_assets = FloatField(default=0, blank=True, null=True)
    other_non_current_assets = FloatField(default=0, blank=True, null=True)
    total_non_current_assets = FloatField(default=0, blank=True, null=True)
    other_assets = FloatField(default=0, blank=True, null=True)
    total_assets = FloatField(default=0, blank=True, null=True)
    accounts_payable = FloatField(default=0, blank=True, null=True)
    short_term_debt = FloatField(default=0, blank=True, null=True)
    tax_payables = FloatField(default=0, blank=True, null=True)
    deferred_revenue = FloatField(default=0, blank=True, null=True)
    other_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_current_liabilities = FloatField(default=0, blank=True, null=True)
    long_term_debt = FloatField(default=0, blank=True, null=True)
    deferred_revenue_non_current = FloatField(default=0, blank=True, null=True)
    deferred_tax_liabilities_non_current = FloatField(default=0, blank=True, null=True)
    other_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    other_liabilities = FloatField(default=0, blank=True, null=True)
    total_liabilities = FloatField(default=0, blank=True, null=True)
    common_stocks = FloatField(default=0, blank=True, null=True)
    preferred_stocks = FloatField(default=0, blank=True, null=True)
    retained_earnings = FloatField(default=0, blank=True, null=True)
    accumulated_other_comprehensive_income_loss = FloatField(default=0, blank=True, null=True)
    othertotal_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_liabilities_and_total_equity = FloatField(default=0, blank=True, null=True)
    total_investments = FloatField(default=0, blank=True, null=True)
    total_debt = FloatField(default=0, blank=True, null=True)
    net_debt = FloatField(default=0, blank=True, null=True)

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
    net_income = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    deferred_income_tax = FloatField(default=0, blank=True, null=True)
    stock_based_compensation = FloatField(
        default=0, blank=True, null=True
    )  # stock_based_compensation
    change_in_working_capital = FloatField(default=0, blank=True, null=True)
    accounts_receivable = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    accounts_payable = FloatField(default=0, blank=True, null=True)
    other_working_capital = FloatField(default=0, blank=True, null=True)
    other_non_cash_items = FloatField(default=0, blank=True, null=True)
    operating_activities_cf = FloatField(default=0, blank=True, null=True)
    investments_property_plant_equipment = FloatField(default=0, blank=True, null=True)
    acquisitions_net = FloatField(default=0, blank=True, null=True)
    purchases_investments = FloatField(default=0, blank=True, null=True)
    sales_maturities_investments = FloatField(default=0, blank=True, null=True)
    other_investing_activites = FloatField(default=0, blank=True, null=True)
    investing_activities_cf = FloatField(default=0, blank=True, null=True)
    debt_repayment = FloatField(default=0, blank=True, null=True)
    common_stock_issued = FloatField(default=0, blank=True, null=True)
    common_stock_repurchased = FloatField(default=0, blank=True, null=True)
    dividends_paid = FloatField(default=0, blank=True, null=True)
    other_financing_activities = FloatField(default=0, blank=True, null=True)
    financing_activities_cf = FloatField(default=0, blank=True, null=True)
    effect_forex_exchange = FloatField(default=0, blank=True, null=True)
    net_change_cash = FloatField(default=0, blank=True, null=True)
    cash_end_period = FloatField(default=0, blank=True, null=True)
    cash_beginning_period = FloatField(default=0, blank=True, null=True)
    operating_cf = FloatField(default=0, blank=True, null=True)
    capex = FloatField(default=0, blank=True, null=True)
    fcf = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Cash flow Statement"
        verbose_name_plural = "Cash flow Statements"
        db_table = "assets_companies_cashflow_statements"

    @property
    def cash_conversion_ratio_to_save(self):
        return self.fcf / self.net_income if self.net_income != 0 else 0


class RentabilityRatio(BaseFinalStatement):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="rentability_ratios",
    )
    roa = FloatField(default=0, blank=True, null=True)
    roe = FloatField(default=0, blank=True, null=True)
    roc = FloatField(default=0, blank=True, null=True)
    roce = FloatField(default=0, blank=True, null=True)
    rota = FloatField(default=0, blank=True, null=True)
    roic = FloatField(default=0, blank=True, null=True)
    nopat_roic = FloatField(default=0, blank=True, null=True)
    rogic = FloatField(default=0, blank=True, null=True)

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
    cash_ratio = FloatField(default=0, blank=True, null=True)
    current_ratio = FloatField(default=0, blank=True, null=True)
    quick_ratio = FloatField(default=0, blank=True, null=True)
    operating_cashflow_ratio = FloatField(default=0, blank=True, null=True)
    debt_to_equity = FloatField(default=0, blank=True, null=True)

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
    gross_margin = FloatField(default=0, blank=True, null=True)
    ebitda_margin = FloatField(default=0, blank=True, null=True)
    net_income_margin = FloatField(default=0, blank=True, null=True)
    fcf_margin = FloatField(default=0, blank=True, null=True)
    fcf_equity_to_net_income = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_to_net_income = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_ebit_to_net_income = FloatField(default=0, blank=True, null=True)
    owners_earnings_to_net_income = FloatField(default=0, blank=True, null=True)

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
    fcf_equity = FloatField(default=0, blank=True, null=True)
    unlevered_fcf = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_ebit = FloatField(default=0, blank=True, null=True)
    owners_earnings = FloatField(default=0, blank=True, null=True)

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
    sales_ps = FloatField(default=0, blank=True, null=True)
    book_ps = FloatField(default=0, blank=True, null=True)
    tangible_ps = FloatField(default=0, blank=True, null=True)
    fcf_ps = FloatField(default=0, blank=True, null=True)
    eps = FloatField(default=0, blank=True, null=True)
    cash_ps = FloatField(default=0, blank=True, null=True)
    operating_cf_ps = FloatField(default=0, blank=True, null=True)
    capex_ps = FloatField(default=0, blank=True, null=True)
    total_assets_ps = FloatField(default=0, blank=True, null=True)

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
    normalized_income = FloatField(default=0, blank=True, null=True)
    effective_tax_rate = FloatField(default=0, blank=True, null=True)
    nopat = FloatField(default=0, blank=True, null=True)
    net_working_cap = FloatField(default=0, blank=True, null=True)
    average_inventory = FloatField(default=0, blank=True, null=True)
    average_accounts_payable = FloatField(default=0, blank=True, null=True)
    dividend_yield = FloatField(default=0, blank=True, null=True)
    earnings_yield = FloatField(default=0, blank=True, null=True)
    fcf_yield = FloatField(default=0, blank=True, null=True)
    income_quality = FloatField(default=0, blank=True, null=True)
    invested_capital = FloatField(default=0, blank=True, null=True)
    market_cap = FloatField(default=0, blank=True, null=True)
    net_current_asset_value = FloatField(default=0, blank=True, null=True)
    payout_ratio = FloatField(default=0, blank=True, null=True)
    tangible_assets = FloatField(default=0, blank=True, null=True)
    retention_ratio = FloatField(default=0, blank=True, null=True)

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
    asset_coverage_ratio = FloatField(default=0, blank=True, null=True)
    cash_flow_coverage_ratios = FloatField(default=0, blank=True, null=True)
    cash_coverage = FloatField(default=0, blank=True, null=True)
    debt_service_coverage = FloatField(default=0, blank=True, null=True)
    interest_coverage = FloatField(default=0, blank=True, null=True)
    operating_cashflow_ratio = FloatField(default=0, blank=True, null=True)
    debt_ratio = FloatField(default=0, blank=True, null=True)
    long_term_debt_to_capitalization = FloatField(default=0, blank=True, null=True)
    total_debt_to_capitalization = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Operation Risk Ratio"
        verbose_name_plural = "Operation Risk Ratios"
        db_table = "assets_companies_operations_risk_ratio"


class EnterpriseValueRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="ev_ratios"
    )
    market_cap = FloatField(default=0, blank=True, null=True)
    enterprise_value = FloatField(default=0, blank=True, null=True)
    ev_fcf = FloatField(default=0, blank=True, null=True)
    ev_operating_cf = FloatField(default=0, blank=True, null=True)
    ev_sales = FloatField(default=0, blank=True, null=True)
    company_equity_multiplier = FloatField(default=0, blank=True, null=True)
    ev_multiple = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Enterprise Value"
        verbose_name_plural = "Enterprise Values"
        db_table = "assets_companies_enterprise_value_ratios"


class CompanyGrowth(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="growth_rates"
    )
    revenue_growth = FloatField(default=0, blank=True, null=True)
    cost_revenue_growth = FloatField(default=0, blank=True, null=True)
    operating_expenses_growth = FloatField(default=0, blank=True, null=True)
    net_income_growth = FloatField(default=0, blank=True, null=True)
    shares_buyback = FloatField(default=0, blank=True, null=True)
    eps_growth = FloatField(default=0, blank=True, null=True)
    fcf_growth = FloatField(default=0, blank=True, null=True)
    owners_earnings_growth = FloatField(default=0, blank=True, null=True)
    capex_growth = FloatField(default=0, blank=True, null=True)
    rd_expenses_growth = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Company growth"
        verbose_name_plural = "Companies growth"
        db_table = "assets_companies_growths"


class EficiencyRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="efficiency_ratios"
    )
    asset_turnover = FloatField(default=0, blank=True, null=True)
    inventory_turnover = FloatField(default=0, blank=True, null=True)
    fixed_asset_turnover = FloatField(default=0, blank=True, null=True)
    accounts_payable_turnover = FloatField(default=0, blank=True, null=True)
    cash_conversion_cycle = FloatField(default=0, blank=True, null=True)
    days_inventory_outstanding = FloatField(default=0, blank=True, null=True)
    days_payables_outstanding = FloatField(default=0, blank=True, null=True)
    days_sales_outstanding = FloatField(default=0, blank=True, null=True)
    free_cashflow_to_operating_cashflow = FloatField(default=0, blank=True, null=True)
    operating_cycle = FloatField(default=0, blank=True, null=True)
    cash_conversion_ratio = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Efficiency Ratio"
        verbose_name_plural = "Efficiency Ratios"
        db_table = "assets_companies_eficiency_ratios"


class PriceToRatio(BaseFinalStatement):
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, blank=True, related_name="price_to_ratios"
    )
    price_book = FloatField(default=0, blank=True, null=True)
    price_cf = FloatField(default=0, blank=True, null=True)
    price_earnings = FloatField(default=0, blank=True, null=True)
    price_earnings_growth = FloatField(default=0, blank=True, null=True)
    price_sales = FloatField(default=0, blank=True, null=True)
    price_total_assets = FloatField(default=0, blank=True, null=True)
    price_fcf = FloatField(default=0, blank=True, null=True)
    price_operating_cf = FloatField(default=0, blank=True, null=True)
    price_tangible_assets = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Price to Ratio"
        verbose_name_plural = "Price to Ratios"
        db_table = "assets_companies_price_to_ratios"
