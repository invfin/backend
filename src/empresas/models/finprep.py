from django.db.models import SET_NULL, FloatField, ForeignKey, DateField, DateTimeField, IntegerField, CharField

from src.empresas.models.statements import BaseStatement
from src.empresas.extensions.finprep import (
    BalanceSheetFinprepExtended,
    CashflowStatementFinprepExtended,
    IncomeStatementFinprepExtended,
)


class BaseFinprep(BaseStatement):
    accepted_date = DateTimeField(blank=True, null=True)
    filling_date = DateField(blank=True, null=True)
    final_link = CharField(max_length=1000, blank=True, null=True)
    link = CharField(max_length=1000, blank=True, null=True)
    reported_currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True, blank=True)
    calendar_year = IntegerField(blank=True, null=True)
    cik = CharField(max_length=100, blank=True, null=True)
    symbol = CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


class IncomeStatementFinprep(BaseFinprep, IncomeStatementFinprepExtended):
    cost_and_expenses = FloatField(default=0, blank=True, null=True)
    cost_of_revenue = FloatField(default=0, blank=True, null=True)
    depreciation_and_amortization = FloatField(default=0, blank=True, null=True)
    ebitda = FloatField(default=0, blank=True, null=True)
    ebitdaratio = FloatField(default=0, blank=True, null=True)
    eps = FloatField(default=0, blank=True, null=True)
    epsdiluted = FloatField(default=0, blank=True, null=True)
    general_and_administrative_expenses = FloatField(default=0, blank=True, null=True)
    gross_profit = FloatField(default=0, blank=True, null=True)
    gross_profit_ratio = FloatField(default=0, blank=True, null=True)
    income_before_tax = FloatField(default=0, blank=True, null=True)
    income_before_tax_ratio = FloatField(default=0, blank=True, null=True)
    income_tax_expense = FloatField(default=0, blank=True, null=True)
    interest_expense = FloatField(default=0, blank=True, null=True)
    interest_income = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    net_income_ratio = FloatField(default=0, blank=True, null=True)
    operating_expenses = FloatField(default=0, blank=True, null=True)
    operating_income = FloatField(default=0, blank=True, null=True)
    operating_income_ratio = FloatField(default=0, blank=True, null=True)
    other_expenses = FloatField(default=0, blank=True, null=True)
    research_and_development_expenses = FloatField(default=0, blank=True, null=True)
    revenue = FloatField(default=0, blank=True, null=True)
    selling_and_marketing_expenses = FloatField(default=0, blank=True, null=True)
    selling_general_and_administrative_expenses = FloatField(default=0, blank=True, null=True)
    total_other_income_expenses_net = FloatField(default=0, blank=True, null=True)
    weighted_average_shs_out = FloatField(default=0, blank=True, null=True)
    weighted_average_shs_out_dil = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Income Statement"
        verbose_name_plural = "Finprep Income Statements"
        db_table = "assets_companies_income_statements_finprep"


class BalanceSheetFinprep(BaseFinprep, BalanceSheetFinprepExtended):
    account_payables = FloatField(default=0, blank=True, null=True)
    accumulated_other_comprehensive_income_loss = FloatField(default=0, blank=True, null=True)
    capital_lease_obligations = FloatField(default=0, blank=True, null=True)
    cash_and_cash_equivalents = FloatField(default=0, blank=True, null=True)
    cash_and_short_term_investments = FloatField(default=0, blank=True, null=True)
    common_stock = FloatField(default=0, blank=True, null=True)
    deferred_revenue = FloatField(default=0, blank=True, null=True)
    deferred_revenue_non_current = FloatField(default=0, blank=True, null=True)
    deferred_tax_liabilities_non_current = FloatField(default=0, blank=True, null=True)
    goodwill = FloatField(default=0, blank=True, null=True)
    goodwill_and_intangible_assets = FloatField(default=0, blank=True, null=True)
    intangible_assets = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    long_term_debt = FloatField(default=0, blank=True, null=True)
    long_term_investments = FloatField(default=0, blank=True, null=True)
    minority_interest = FloatField(default=0, blank=True, null=True)
    net_debt = FloatField(default=0, blank=True, null=True)
    net_receivables = FloatField(default=0, blank=True, null=True)
    other_assets = FloatField(default=0, blank=True, null=True)
    other_current_assets = FloatField(default=0, blank=True, null=True)
    other_current_liabilities = FloatField(default=0, blank=True, null=True)
    other_liabilities = FloatField(default=0, blank=True, null=True)
    other_non_current_assets = FloatField(default=0, blank=True, null=True)
    other_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    othertotal_stockholders_equity = FloatField(default=0, blank=True, null=True)
    preferred_stock = FloatField(default=0, blank=True, null=True)
    property_plant_equipment_net = FloatField(default=0, blank=True, null=True)
    retained_earnings = FloatField(default=0, blank=True, null=True)
    short_term_debt = FloatField(default=0, blank=True, null=True)
    short_term_investments = FloatField(default=0, blank=True, null=True)
    tax_assets = FloatField(default=0, blank=True, null=True)
    tax_payables = FloatField(default=0, blank=True, null=True)
    total_assets = FloatField(default=0, blank=True, null=True)
    total_current_assets = FloatField(default=0, blank=True, null=True)
    total_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_debt = FloatField(default=0, blank=True, null=True)
    total_equity = FloatField(default=0, blank=True, null=True)
    total_investments = FloatField(default=0, blank=True, null=True)
    total_liabilities = FloatField(default=0, blank=True, null=True)
    total_liabilities_and_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_liabilities_and_total_equity = FloatField(default=0, blank=True, null=True)
    total_non_current_assets = FloatField(default=0, blank=True, null=True)
    total_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_stockholders_equity = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Balance Sheet"
        verbose_name_plural = "Finprep Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_finprep"


class CashflowStatementFinprep(BaseFinprep, CashflowStatementFinprepExtended):
    accounts_payables = FloatField(default=0, blank=True, null=True)
    accounts_receivables = FloatField(default=0, blank=True, null=True)
    acquisitions_net = FloatField(default=0, blank=True, null=True)
    capital_expenditure = FloatField(default=0, blank=True, null=True)
    cash_at_beginning_of_period = FloatField(default=0, blank=True, null=True)
    cash_at_end_of_period = FloatField(default=0, blank=True, null=True)
    change_in_working_capital = FloatField(default=0, blank=True, null=True)
    common_stock_issued = FloatField(default=0, blank=True, null=True)
    common_stock_repurchased = FloatField(default=0, blank=True, null=True)
    debt_repayment = FloatField(default=0, blank=True, null=True)
    deferred_income_tax = FloatField(default=0, blank=True, null=True)
    depreciation_and_amortization = FloatField(default=0, blank=True, null=True)
    dividends_paid = FloatField(default=0, blank=True, null=True)
    effect_of_forex_changes_on_cash = FloatField(default=0, blank=True, null=True)
    free_cash_flow = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    investments_in_property_plant_and_equipment = FloatField(default=0, blank=True, null=True)
    net_cash_provided_by_operating_activities = FloatField(default=0, blank=True, null=True)
    net_cash_used_for_investing_activites = FloatField(default=0, blank=True, null=True)
    net_cash_used_provided_by_financing_activities = FloatField(default=0, blank=True, null=True)
    net_change_in_cash = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    operating_cash_flow = FloatField(default=0, blank=True, null=True)
    other_financing_activites = FloatField(default=0, blank=True, null=True)
    other_investing_activites = FloatField(default=0, blank=True, null=True)
    other_non_cash_items = FloatField(default=0, blank=True, null=True)
    other_working_capital = FloatField(default=0, blank=True, null=True)
    purchases_of_investments = FloatField(default=0, blank=True, null=True)
    sales_maturities_of_investments = FloatField(default=0, blank=True, null=True)
    stock_based_compensation = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Cash flow Statement"
        verbose_name_plural = "Finprep Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_finprep"

    @property
    def cash_conversion_ratio_to_save(self):
        return self.fcf / self.net_income if self.net_income != 0 else 0
