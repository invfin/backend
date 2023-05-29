from django.db.models import (
    SET_NULL,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    IntegerField,
)

from src.empresas.extensions.finprep import (
    BalanceSheetFinprepExtended,
    CashflowStatementFinprepExtended,
    IncomeStatementFinprepExtended,
)
from src.empresas.models.statements import BaseStatement
from src.empresas.fields import EntryStatementField


class BaseFinprep(BaseStatement):
    accepted_date = DateTimeField(blank=True, null=True)
    filling_date = DateField(blank=True, null=True)
    final_link = CharField(max_length=1000, blank=True, null=True)
    link = CharField(max_length=1000, blank=True, null=True)
    reported_currency = ForeignKey(
        "currencies.Currency", on_delete=SET_NULL, null=True, blank=True
    )
    calendar_year = IntegerField(blank=True, null=True)
    cik = CharField(max_length=100, blank=True, null=True)
    symbol = CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


class IncomeStatementFinprep(BaseFinprep, IncomeStatementFinprepExtended):
    cost_and_expenses = EntryStatementField()
    cost_of_revenue = EntryStatementField()
    depreciation_and_amortization = EntryStatementField()
    ebitda = EntryStatementField()
    ebitdaratio = EntryStatementField()
    eps = EntryStatementField()
    epsdiluted = EntryStatementField()
    general_and_administrative_expenses = EntryStatementField()
    gross_profit = EntryStatementField()
    gross_profit_ratio = EntryStatementField()
    income_before_tax = EntryStatementField()
    income_before_tax_ratio = EntryStatementField()
    income_tax_expense = EntryStatementField()
    interest_expense = EntryStatementField()
    interest_income = EntryStatementField()
    net_income = EntryStatementField()
    net_income_ratio = EntryStatementField()
    operating_expenses = EntryStatementField()
    operating_income = EntryStatementField()
    operating_income_ratio = EntryStatementField()
    other_expenses = EntryStatementField()
    research_and_development_expenses = EntryStatementField()
    revenue = EntryStatementField()
    selling_and_marketing_expenses = EntryStatementField()
    selling_general_and_administrative_expenses = EntryStatementField()
    total_other_income_expenses_net = EntryStatementField()
    weighted_average_shs_out = EntryStatementField()
    weighted_average_shs_out_dil = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Income Statement"
        verbose_name_plural = "Finprep Income Statements"
        db_table = "assets_companies_income_statements_finprep"


class BalanceSheetFinprep(BaseFinprep, BalanceSheetFinprepExtended):
    account_payables = EntryStatementField()
    accumulated_other_comprehensive_income_loss = EntryStatementField()
    capital_lease_obligations = EntryStatementField()
    cash_and_cash_equivalents = EntryStatementField()
    cash_and_short_term_investments = EntryStatementField()
    common_stock = EntryStatementField()
    deferred_revenue = EntryStatementField()
    deferred_revenue_non_current = EntryStatementField()
    deferred_tax_liabilities_non_current = EntryStatementField()
    goodwill = EntryStatementField()
    goodwill_and_intangible_assets = EntryStatementField()
    intangible_assets = EntryStatementField()
    inventory = EntryStatementField()
    long_term_debt = EntryStatementField()
    long_term_investments = EntryStatementField()
    minority_interest = EntryStatementField()
    net_debt = EntryStatementField()
    net_receivables = EntryStatementField()
    other_assets = EntryStatementField()
    other_current_assets = EntryStatementField()
    other_current_liabilities = EntryStatementField()
    other_liabilities = EntryStatementField()
    other_non_current_assets = EntryStatementField()
    other_non_current_liabilities = EntryStatementField()
    othertotal_stockholders_equity = EntryStatementField()
    preferred_stock = EntryStatementField()
    property_plant_equipment_net = EntryStatementField()
    retained_earnings = EntryStatementField()
    short_term_debt = EntryStatementField()
    short_term_investments = EntryStatementField()
    tax_assets = EntryStatementField()
    tax_payables = EntryStatementField()
    total_assets = EntryStatementField()
    total_current_assets = EntryStatementField()
    total_current_liabilities = EntryStatementField()
    total_debt = EntryStatementField()
    total_equity = EntryStatementField()
    total_investments = EntryStatementField()
    total_liabilities = EntryStatementField()
    total_liabilities_and_stockholders_equity = EntryStatementField()
    total_liabilities_and_total_equity = EntryStatementField()
    total_non_current_assets = EntryStatementField()
    total_non_current_liabilities = EntryStatementField()
    total_stockholders_equity = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Balance Sheet"
        verbose_name_plural = "Finprep Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_finprep"


class CashflowStatementFinprep(BaseFinprep, CashflowStatementFinprepExtended):
    accounts_payables = EntryStatementField()
    accounts_receivables = EntryStatementField()
    acquisitions_net = EntryStatementField()
    capital_expenditure = EntryStatementField()
    cash_at_beginning_of_period = EntryStatementField()
    cash_at_end_of_period = EntryStatementField()
    change_in_working_capital = EntryStatementField()
    common_stock_issued = EntryStatementField()
    common_stock_repurchased = EntryStatementField()
    debt_repayment = EntryStatementField()
    deferred_income_tax = EntryStatementField()
    depreciation_and_amortization = EntryStatementField()
    dividends_paid = EntryStatementField()
    effect_of_forex_changes_on_cash = EntryStatementField()
    free_cash_flow = EntryStatementField()
    inventory = EntryStatementField()
    investments_in_property_plant_and_equipment = EntryStatementField()
    net_cash_provided_by_operating_activities = EntryStatementField()
    net_cash_used_for_investing_activites = EntryStatementField()
    net_cash_used_provided_by_financing_activities = EntryStatementField()
    net_change_in_cash = EntryStatementField()
    net_income = EntryStatementField()
    operating_cash_flow = EntryStatementField()
    other_financing_activites = EntryStatementField()
    other_investing_activites = EntryStatementField()
    other_non_cash_items = EntryStatementField()
    other_working_capital = EntryStatementField()
    purchases_of_investments = EntryStatementField()
    sales_maturities_of_investments = EntryStatementField()
    stock_based_compensation = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Cash flow Statement"
        verbose_name_plural = "Finprep Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_finprep"

    @property
    def cash_conversion_ratio_to_save(self):
        return self.fcf / self.net_income if self.net_income != 0 else 0
