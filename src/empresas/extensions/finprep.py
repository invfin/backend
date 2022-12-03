from .base_averages import AverageBalanceSheet, AverageCashflowStatement, AverageIncomeStatement


class IncomeStatementFinprepExtended(AverageIncomeStatement):
    rd_expenses_field = "research_and_development_expenses"
    general_administrative_expenses_field = "general_and_administrative_expenses"
    selling_marketing_expenses_field = "selling_and_marketing_expenses"
    sga_expenses_field = "selling_general_and_administrative_expenses"
    depreciation_amortization_field = "depreciation_and_amortization"
    net_total_other_income_expenses_field = "total_other_income_expenses_net"
    weighted_average_shares_outstanding_field = "weighted_average_shs_out"
    weighted_average_diluated_shares_outstanding_field = "weighted_average_shs_out_dil"
    income_tax_expenses_field = "income_tax_expense"


class BalanceSheetFinprepExtended(AverageBalanceSheet):
    property_plant_equipment_field = "property_plant_equipment_net"
    common_stocks_field = "common_stock"


class CashflowStatementFinprepExtended(AverageCashflowStatement):
    depreciation_amortization_field = "depreciation_and_amortization"
    stock_based_compesation_field = "stock_based_compensation"
    accounts_payable_field = "accounts_payables"
    operating_activities_cf_field = "net_cash_provided_by_operating_activities"
    investments_property_plant_equipment_field = "investments_in_property_plant_and_equipment"
    purchases_investments_field = "purchases_of_investments"
    sales_maturities_investments_field = "sales_maturities_of_investments"
    investing_activities_cf_field = "net_cash_used_for_investing_activites"
    other_financing_activities_field = "other_financing_activites"
    financing_activities_cf_field = "net_cash_used_provided_by_financing_activities"
    effect_forex_exchange_field = "effect_of_forex_changes_on_cash"
    net_change_cash_field = "net_change_in_cash"
    cash_end_period_field = "cash_at_end_of_period"
    cash_beginning_period_field = "cash_at_beginning_of_period"
    operating_cf_field = "operating_cash_flow"
    capex_field = "capital_expenditure"
    fcf_field = "free_cash_flow"
