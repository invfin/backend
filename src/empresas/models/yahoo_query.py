from django.db.models import CharField, DateTimeField, JSONField

from src.empresas.extensions.yahoo_query import (
    BalanceSheetYahooQueryExtended,
    CashflowStatementYahooQueryExtended,
    IncomeStatementYahooQueryExtended,
)
from src.empresas.models import BaseStatement
from src.empresas.fields import EntryStatementField


class BaseUnknownField(BaseStatement):
    financials = JSONField(default=dict)

    class Meta:
        abstract = True


class IncomeStatementYahooQuery(BaseUnknownField, IncomeStatementYahooQueryExtended):
    as_of_date = DateTimeField(blank=True, null=True)
    period_type = CharField(max_length=10, blank=True, null=True)
    currency_code = CharField(max_length=10, blank=True, null=True)
    basic_average_shares = EntryStatementField()
    basic_eps = EntryStatementField()
    cost_of_revenue = EntryStatementField()
    diluted_average_shares = EntryStatementField()
    diluted_eps = EntryStatementField()
    diluted_ni_availto_com_stockholders = EntryStatementField()
    ebit = EntryStatementField()
    ebitda = EntryStatementField()
    gross_profit = EntryStatementField()
    interest_expense = EntryStatementField()
    interest_expense_non_operating = EntryStatementField()
    interest_income = EntryStatementField()
    interest_income_non_operating = EntryStatementField()
    net_income = EntryStatementField()
    net_income_common_stockholders = EntryStatementField()
    net_income_continuous_operations = EntryStatementField()
    net_income_from_continuing_and_discontinued_operation = EntryStatementField()
    net_income_from_continuing_operation_net_minority_interest = EntryStatementField()
    net_income_including_noncontrolling_interests = EntryStatementField()
    net_interest_income = EntryStatementField()
    net_non_operating_interest_income_expense = EntryStatementField()
    normalized_ebitda = EntryStatementField()
    normalized_income = EntryStatementField()
    operating_expense = EntryStatementField()
    operating_income = EntryStatementField()
    operating_revenue = EntryStatementField()
    other_income_expense = EntryStatementField()
    other_non_operating_income_expenses = EntryStatementField()
    pretax_income = EntryStatementField()
    reconciled_cost_of_revenue = EntryStatementField()
    reconciled_depreciation = EntryStatementField()
    research_and_development = EntryStatementField()
    selling_general_and_administration = EntryStatementField()
    tax_effect_of_unusual_items = EntryStatementField()
    tax_provision = EntryStatementField()
    tax_rate_for_calcs = EntryStatementField()
    total_expenses = EntryStatementField()
    total_operating_income_as_reported = EntryStatementField()
    total_revenue = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Yahooquery Income Statement"
        verbose_name_plural = "Yahooquery Income Statements"
        db_table = "assets_companies_income_statements_yahooquery"


class BalanceSheetYahooQuery(BaseUnknownField, BalanceSheetYahooQueryExtended):
    as_of_date = DateTimeField(blank=True, null=True)
    period_type = CharField(max_length=10, blank=True, null=True)
    currency_code = CharField(max_length=10, blank=True, null=True)
    accounts_payable = EntryStatementField()
    accounts_receivable = EntryStatementField()
    accumulated_depreciation = EntryStatementField()
    available_for_sale_securities = EntryStatementField()
    capital_stock = EntryStatementField()
    cash_and_cash_equivalents = EntryStatementField()
    cash_cash_equivalents_and_short_term_investments = EntryStatementField()
    cash_equivalents = EntryStatementField()
    cash_financial = EntryStatementField()
    commercial_paper = EntryStatementField()
    common_stock = EntryStatementField()
    common_stock_equity = EntryStatementField()
    current_assets = EntryStatementField()
    current_debt = EntryStatementField()
    current_debt_and_capital_lease_obligation = EntryStatementField()
    current_deferred_liabilities = EntryStatementField()
    current_deferred_revenue = EntryStatementField()
    current_liabilities = EntryStatementField()
    gains_losses_not_affecting_retained_earnings = EntryStatementField()
    gross_ppe = EntryStatementField()
    inventory = EntryStatementField()
    invested_capital = EntryStatementField()
    investmentin_financial_assets = EntryStatementField()
    investments_and_advances = EntryStatementField()
    land_and_improvements = EntryStatementField()
    leases = EntryStatementField()
    long_term_debt = EntryStatementField()
    long_term_debt_and_capital_lease_obligation = EntryStatementField()
    machinery_furniture_equipment = EntryStatementField()
    net_debt = EntryStatementField()
    net_ppe = EntryStatementField()
    net_tangible_assets = EntryStatementField()
    non_current_deferred_liabilities = EntryStatementField()
    non_current_deferred_revenue = EntryStatementField()
    non_current_deferred_taxes_liabilities = EntryStatementField()
    ordinary_shares_number = EntryStatementField()
    other_current_assets = EntryStatementField()
    other_current_borrowings = EntryStatementField()
    other_current_liabilities = EntryStatementField()
    other_non_current_assets = EntryStatementField()
    other_non_current_liabilities = EntryStatementField()
    other_receivables = EntryStatementField()
    other_short_term_investments = EntryStatementField()
    payables = EntryStatementField()
    payables_and_accrued_expenses = EntryStatementField()
    properties = EntryStatementField()
    receivables = EntryStatementField()
    retained_earnings = EntryStatementField()
    share_issued = EntryStatementField()
    stockholders_equity = EntryStatementField()
    tangible_book_value = EntryStatementField()
    total_assets = EntryStatementField()
    total_capitalization = EntryStatementField()
    total_debt = EntryStatementField()
    total_equity_gross_minority_interest = EntryStatementField()
    total_liabilities_net_minority_interest = EntryStatementField()
    total_non_current_assets = EntryStatementField()
    total_non_current_liabilities_net_minority_interest = EntryStatementField()
    tradeand_other_payables_non_current = EntryStatementField()
    working_capital = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Yahooquery Balance Sheet"
        verbose_name_plural = "Yahooquery Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_yahooquery"


class CashflowStatementYahooQuery(BaseUnknownField, CashflowStatementYahooQueryExtended):
    as_of_date = DateTimeField(blank=True, null=True)
    period_type = CharField(max_length=10, blank=True, null=True)
    currency_code = CharField(max_length=10, blank=True, null=True)
    beginning_cash_position = EntryStatementField()
    capital_expenditure = EntryStatementField()
    cash_dividends_paid = EntryStatementField()
    cash_flow_from_continuing_financing_activities = EntryStatementField()
    cash_flow_from_continuing_investing_activities = EntryStatementField()
    cash_flow_from_continuing_operating_activities = EntryStatementField()
    change_in_account_payable = EntryStatementField()
    change_in_cash_supplemental_as_reported = EntryStatementField()
    change_in_inventory = EntryStatementField()
    change_in_other_current_assets = EntryStatementField()
    change_in_other_current_liabilities = EntryStatementField()
    change_in_other_working_capital = EntryStatementField()
    change_in_payable = EntryStatementField()
    change_in_payables_and_accrued_expense = EntryStatementField()
    change_in_receivables = EntryStatementField()
    change_in_working_capital = EntryStatementField()
    changes_in_account_receivables = EntryStatementField()
    changes_in_cash = EntryStatementField()
    common_stock_dividend_paid = EntryStatementField()
    common_stock_issuance = EntryStatementField()
    common_stock_payments = EntryStatementField()
    deferred_income_tax = EntryStatementField()
    deferred_tax = EntryStatementField()
    depreciation_amortization_depletion = EntryStatementField()
    depreciation_and_amortization = EntryStatementField()
    end_cash_position = EntryStatementField()
    financing_cash_flow = EntryStatementField()
    free_cash_flow = EntryStatementField()
    income_tax_paid_supplemental_data = EntryStatementField()
    interest_paid_supplemental_data = EntryStatementField()
    investing_cash_flow = EntryStatementField()
    issuance_of_capital_stock = EntryStatementField()
    issuance_of_debt = EntryStatementField()
    long_term_debt_issuance = EntryStatementField()
    long_term_debt_payments = EntryStatementField()
    net_business_purchase_and_sale = EntryStatementField()
    net_common_stock_issuance = EntryStatementField()
    net_income = EntryStatementField()
    net_income_from_continuing_operations = EntryStatementField()
    net_investment_purchase_and_sale = EntryStatementField()
    net_issuance_payments_of_debt = EntryStatementField()
    net_long_term_debt_issuance = EntryStatementField()
    net_other_financing_charges = EntryStatementField()
    net_other_investing_changes = EntryStatementField()
    net_ppe_purchase_and_sale = EntryStatementField()
    net_short_term_debt_issuance = EntryStatementField()
    operating_cash_flow = EntryStatementField()
    other_non_cash_items = EntryStatementField()
    purchase_of_business = EntryStatementField()
    purchase_of_investment = EntryStatementField()
    purchase_of_ppe = EntryStatementField()
    repayment_of_debt = EntryStatementField()
    repurchase_of_capital_stock = EntryStatementField()
    sale_of_investment = EntryStatementField()
    short_term_debt_payments = EntryStatementField()
    stock_based_compensation = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Yahooquery Cash flow Statement"
        verbose_name_plural = "Yahooquery Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_yahooquery"


class KeyStatsYahooQuery(BaseUnknownField):
    reported_currency = None
    max_age = EntryStatementField()
    price_hint = EntryStatementField()
    enterprise_value = EntryStatementField()
    forward_pe = EntryStatementField()
    profit_margins = EntryStatementField()
    float_shares = EntryStatementField()
    shares_outstanding = EntryStatementField()
    shares_short = EntryStatementField()
    shares_short_prior_month = EntryStatementField()
    shares_short_previous_month_date = DateTimeField(blank=True, null=True)
    date_short_interest = DateTimeField(blank=True, null=True)
    shares_percent_shares_out = EntryStatementField()
    held_percent_insiders = EntryStatementField()
    held_percent_institutions = EntryStatementField()
    short_ratio = EntryStatementField()
    short_percent_of_float = EntryStatementField()
    beta = EntryStatementField()
    category = EntryStatementField()
    book_value = EntryStatementField()
    price_to_book = EntryStatementField()
    fund_family = EntryStatementField()
    legal_type = EntryStatementField()
    last_fiscal_year_end = DateTimeField(blank=True, null=True)
    next_fiscal_year_end = DateTimeField(blank=True, null=True)
    most_recent_quarter = DateTimeField(blank=True, null=True)
    earnings_quarterly_growth = EntryStatementField()
    net_income_to_common = EntryStatementField()
    trailing_eps = EntryStatementField()
    forward_eps = EntryStatementField()
    peg_ratio = EntryStatementField()
    last_split_factor = CharField(max_length=10, blank=True, null=True)
    last_split_date = DateTimeField(blank=True, null=True)
    enterprise_to_revenue = EntryStatementField()
    enterprise_to_ebitda = EntryStatementField()
    week_change_52 = EntryStatementField()
    sand_p52_week_change = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "Yahooquery Key stats"
        verbose_name_plural = "Yahooquery Key stats"
        db_table = "assets_companies_key_stats_yahooquery"
        get_latest_by = ["-date"]
        ordering = ["-date"]
