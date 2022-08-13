from django.db.models import (
    SET_NULL,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    IntegerField,
    Model,
)

from apps.empresas.models.base import BaseStatement, Company


class BalanceSheetYFinance():
    intangible_assets
    total_liab
    total_stockholder_equity
    other_current_liab
    total_assets
    common_stock
    other_current_assets
    retained_earnings
    other_liab
    good_will
    gains_losses_not_affecting_retained_earnings
    other_assets
    cash
    total_current_liabilities
    deferred_long_term_asset_charges
    short_long_term_debt
    other_stockholder_equity
    property_plant_equipment
    total_current_assets
    long_term_investments
    net_tangible_assets
    short_term_investments
    net_receivables
    long_term_debt
    inventory
    accounts_payable



class CashflowStatementYFinance():
    investments
    change_to_liabilities
    total_cashflows_from_investing_activities
    net_borrowings
    total_cash_from_financing_activities
    change_to_operating_activities
    issuance_of_stock
    net_income
    change_in_cash
    repurchase_of_stock
    effect_of_exchange_rate
    total_cash_from_operating_activities
    depreciation
    other_cashflows_from_investing_activities
    dividends_paid
    change_to_inventory
    change_to_account_receivables
    other_cashflows_from_financing_activities
    change_to_netincome
    capital_expenditures


class IncomeStatementYFinance():
    research_development
effect_of_accounting_charges
income_before_tax
minority_interest
net_income
selling_general_administrative
gross_profit
ebit
operating_income
other_operating_expenses
interest_expense
extraordinary_items
non_recurring
other_items
income_tax_expense
total_revenue
total_operating_expenses
cost_of_revenue
total_other_income_expense_net
discontinued_operations
net_income_from_continuing_ops
net_income_applicable_to_common_shares
