from django.db.models import FloatField, JSONField

from apps.empresas.models import BaseStatement
from apps.empresas.extensions.y_finance import (
    BalanceSheetYFinanceExtended,
    CashflowStatementYFinanceExtended,
    IncomeStatementYFinanceExtended
)

class BaseUnknownField(BaseStatement):
    financials = JSONField(default=dict)

    class Meta:
        abstract = True


class IncomeStatementYFinance(BaseUnknownField, IncomeStatementYFinanceExtended):
    research_development = FloatField(default=0, blank=True, null=True)
    effect_of_accounting_charges = FloatField(default=0, blank=True, null=True)
    income_before_tax = FloatField(default=0, blank=True, null=True)
    minority_interest = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    selling_general_administrative = FloatField(default=0, blank=True, null=True)
    gross_profit = FloatField(default=0, blank=True, null=True)
    ebit = FloatField(default=0, blank=True, null=True)
    operating_income = FloatField(default=0, blank=True, null=True)
    other_operating_expenses = FloatField(default=0, blank=True, null=True)
    interest_expense = FloatField(default=0, blank=True, null=True)
    extraordinary_items = FloatField(default=0, blank=True, null=True)
    non_recurring = FloatField(default=0, blank=True, null=True)
    other_items = FloatField(default=0, blank=True, null=True)
    income_tax_expense = FloatField(default=0, blank=True, null=True)
    total_revenue = FloatField(default=0, blank=True, null=True)
    total_operating_expenses = FloatField(default=0, blank=True, null=True)
    cost_of_revenue = FloatField(default=0, blank=True, null=True)
    total_other_income_expense_net = FloatField(default=0, blank=True, null=True)
    discontinued_operations = FloatField(default=0, blank=True, null=True)
    net_income_from_continuing_ops = FloatField(default=0, blank=True, null=True)
    net_income_applicable_to_common_shares = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Income Statement"
        verbose_name_plural = "YFinance Income Statements"
        db_table = "assets_companies_income_statements_yfinance"

    def __str__(self):
        return self.company.ticker + str(self.date)


class BalanceSheetYFinance(BaseUnknownField, BalanceSheetYFinanceExtended):
    intangible_assets = FloatField(default=0, blank=True, null=True)
    total_liab = FloatField(default=0, blank=True, null=True)
    total_stockholder_equity = FloatField(default=0, blank=True, null=True)
    other_current_liab = FloatField(default=0, blank=True, null=True)
    total_assets = FloatField(default=0, blank=True, null=True)
    common_stock = FloatField(default=0, blank=True, null=True)
    other_current_assets = FloatField(default=0, blank=True, null=True)
    retained_earnings = FloatField(default=0, blank=True, null=True)
    other_liab = FloatField(default=0, blank=True, null=True)
    good_will = FloatField(default=0, blank=True, null=True)
    gains_losses_not_affecting_retained_earnings = FloatField(default=0, blank=True, null=True)
    other_assets = FloatField(default=0, blank=True, null=True)
    cash = FloatField(default=0, blank=True, null=True)
    total_current_liabilities = FloatField(default=0, blank=True, null=True)
    deferred_long_term_asset_charges = FloatField(default=0, blank=True, null=True)
    short_long_term_debt = FloatField(default=0, blank=True, null=True)
    other_stockholder_equity = FloatField(default=0, blank=True, null=True)
    property_plant_equipment = FloatField(default=0, blank=True, null=True)
    total_current_assets = FloatField(default=0, blank=True, null=True)
    long_term_investments = FloatField(default=0, blank=True, null=True)
    net_tangible_assets = FloatField(default=0, blank=True, null=True)
    short_term_investments = FloatField(default=0, blank=True, null=True)
    net_receivables = FloatField(default=0, blank=True, null=True)
    long_term_debt = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    accounts_payable = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Balance Sheet"
        verbose_name_plural = "YFinance Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_yfinance"

    def __str__(self):
        return self.company.ticker + str(self.date)


class CashflowStatementYFinance(BaseUnknownField, CashflowStatementYFinanceExtended):
    investments = FloatField(default=0, blank=True, null=True)
    change_to_liabilities = FloatField(default=0, blank=True, null=True)
    total_cashflows_from_investing_activities = FloatField(default=0, blank=True, null=True)
    net_borrowings = FloatField(default=0, blank=True, null=True)
    total_cash_from_financing_activities = FloatField(default=0, blank=True, null=True)
    change_to_operating_activities = FloatField(default=0, blank=True, null=True)
    issuance_of_stock = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    change_in_cash = FloatField(default=0, blank=True, null=True)
    repurchase_of_stock = FloatField(default=0, blank=True, null=True)
    effect_of_exchange_rate = FloatField(default=0, blank=True, null=True)
    total_cash_from_operating_activities = FloatField(default=0, blank=True, null=True)
    depreciation = FloatField(default=0, blank=True, null=True)
    other_cashflows_from_investing_activities = FloatField(default=0, blank=True, null=True)
    dividends_paid = FloatField(default=0, blank=True, null=True)
    change_to_inventory = FloatField(default=0, blank=True, null=True)
    change_to_account_receivables = FloatField(default=0, blank=True, null=True)
    other_cashflows_from_financing_activities = FloatField(default=0, blank=True, null=True)
    change_to_netincome = FloatField(default=0, blank=True, null=True)
    capital_expenditures = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "YFinance Cash flow Statement"
        verbose_name_plural = "YFinance Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_yfinance"

    def __str__(self):
        return self.company.ticker + str(self.date)
