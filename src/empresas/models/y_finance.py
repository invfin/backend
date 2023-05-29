from django.db.models import JSONField

from src.empresas.extensions.y_finance import (
    BalanceSheetYFinanceExtended,
    CashflowStatementYFinanceExtended,
    IncomeStatementYFinanceExtended,
)
from src.empresas.models import BaseStatement
from src.empresas.fields import EntryStatementField


class BaseUnknownField(BaseStatement):
    financials = JSONField(default=dict)

    class Meta:
        abstract = True


class IncomeStatementYFinance(BaseUnknownField, IncomeStatementYFinanceExtended):
    research_development = EntryStatementField()
    effect_of_accounting_charges = EntryStatementField()
    income_before_tax = EntryStatementField()
    minority_interest = EntryStatementField()
    net_income = EntryStatementField()
    selling_general_administrative = EntryStatementField()
    gross_profit = EntryStatementField()
    ebit = EntryStatementField()
    operating_income = EntryStatementField()
    other_operating_expenses = EntryStatementField()
    interest_expense = EntryStatementField()
    extraordinary_items = EntryStatementField()
    non_recurring = EntryStatementField()
    other_items = EntryStatementField()
    income_tax_expense = EntryStatementField()
    total_revenue = EntryStatementField()
    total_operating_expenses = EntryStatementField()
    cost_of_revenue = EntryStatementField()
    total_other_income_expense_net = EntryStatementField()
    discontinued_operations = EntryStatementField()
    net_income_from_continuing_ops = EntryStatementField()
    net_income_applicable_to_common_shares = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Income Statement"
        verbose_name_plural = "YFinance Income Statements"
        db_table = "assets_companies_income_statements_yfinance"


class BalanceSheetYFinance(BaseUnknownField, BalanceSheetYFinanceExtended):
    intangible_assets = EntryStatementField()
    total_liab = EntryStatementField()
    total_stockholder_equity = EntryStatementField()
    other_current_liab = EntryStatementField()
    total_assets = EntryStatementField()
    common_stock = EntryStatementField()
    other_current_assets = EntryStatementField()
    retained_earnings = EntryStatementField()
    other_liab = EntryStatementField()
    good_will = EntryStatementField()
    gains_losses_not_affecting_retained_earnings = EntryStatementField()
    other_assets = EntryStatementField()
    cash = EntryStatementField()
    total_current_liabilities = EntryStatementField()
    deferred_long_term_asset_charges = EntryStatementField()
    short_long_term_debt = EntryStatementField()
    other_stockholder_equity = EntryStatementField()
    property_plant_equipment = EntryStatementField()
    total_current_assets = EntryStatementField()
    long_term_investments = EntryStatementField()
    net_tangible_assets = EntryStatementField()
    short_term_investments = EntryStatementField()
    net_receivables = EntryStatementField()
    long_term_debt = EntryStatementField()
    inventory = EntryStatementField()
    accounts_payable = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Balance Sheet"
        verbose_name_plural = "YFinance Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_yfinance"


class CashflowStatementYFinance(BaseUnknownField, CashflowStatementYFinanceExtended):
    investments = EntryStatementField()
    change_to_liabilities = EntryStatementField()
    total_cashflows_from_investing_activities = EntryStatementField()
    net_borrowings = EntryStatementField()
    total_cash_from_financing_activities = EntryStatementField()
    change_to_operating_activities = EntryStatementField()
    issuance_of_stock = EntryStatementField()
    net_income = EntryStatementField()
    change_in_cash = EntryStatementField()
    repurchase_of_stock = EntryStatementField()
    effect_of_exchange_rate = EntryStatementField()
    total_cash_from_operating_activities = EntryStatementField()
    depreciation = EntryStatementField()
    other_cashflows_from_investing_activities = EntryStatementField()
    dividends_paid = EntryStatementField()
    change_to_inventory = EntryStatementField()
    change_to_account_receivables = EntryStatementField()
    other_cashflows_from_financing_activities = EntryStatementField()
    change_to_netincome = EntryStatementField()
    capital_expenditures = EntryStatementField()

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Cash flow Statement"
        verbose_name_plural = "YFinance Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_yfinance"
