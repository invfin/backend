from .base_normalize import NormalizeBalanceSheet, NormalizeCashflowStatement, NormalizeIncomeStatement


class IncomeStatementYahooQueryExtended(NormalizeIncomeStatement):
    revenue_field = "total_revenue"
    cost_of_revenue_field = "reconciled_cost_of_revenue"
    gross_profit_field = "gross_profit"
    rd_expenses_field = "research_and_development"
    general_administrative_expenses_field = ""
    selling_marketing_expenses_field = ""
    sga_expenses_field = "selling_general_and_administration"
    other_expenses_field = "other_income_expense"
    operating_expenses_field = "operating_expense"
    cost_and_expenses_field = "total_expenses"
    interest_expense_field = "interest_expense_non_operating"
    depreciation_amortization_field = "reconciled_depreciation"
    ebitda_field = "normalized_ebitda"
    operating_income_field = "total_operating_income_as_reported"
    net_total_other_income_expenses_field = "operating_expense"
    income_before_tax_field = "pretax_income"
    income_tax_expenses_field = "tax_provision"
    net_income_field = "normalized_income"
    weighted_average_shares_outstanding_field = "basic_average_shares"
    weighted_average_diluated_shares_outstanding_field = "diluted_average_shares"


class BalanceSheetYahooQueryExtended(NormalizeBalanceSheet):
    cash_and_cash_equivalents_field = "cash_and_cash_equivalents"
    short_term_investments_field = "other_short_term_investments"
    cash_and_short_term_investments_field = "cash_cash_equivalents_and_short_term_investments"
    net_receivables_field = "receivables"
    inventory_field = "inventory"
    other_current_assets_field = "other_current_assets"
    total_current_assets_field = "current_assets"
    property_plant_equipment_field = "net_ppe"
    goodwill_field = ""
    intangible_assets_field = ""
    goodwill_and_intangible_assets_field = ""
    long_term_investments_field = "investments_and_advances"
    tax_assets_field = ""
    other_non_current_assets_field = "other_non_current_assets"
    total_non_current_assets_field = "total_non_current_assets"
    other_assets_field = ""
    total_assets_field = "total_assets"
    accounts_payable_field = "payables_and_accrued_expenses"
    short_term_debt_field = "current_debt_and_capital_lease_obligation"
    tax_payables_field = ""
    deferred_revenue_field = "current_deferred_revenue"
    other_current_liabilities_field = "other_current_liabilities"
    total_current_liabilities_field = "current_liabilities"
    long_term_debt_field = "long_term_debt_and_capital_lease_obligation"
    deferred_revenue_non_current_field = ""
    deferred_tax_liabilities_non_current_field = ""
    other_non_current_liabilities_field = "other_non_current_liabilities"
    total_non_current_liabilities_field = "total_non_current_liabilities_net_minority_interest"
    other_liabilities_field = ""
    total_liabilities_field = "total_liabilities_net_minority_interest"
    common_stocks_field = "common_stock"
    retained_earnings_field = "retained_earnings"
    accumulated_other_comprehensive_income_loss_field = "gains_losses_not_affecting_retained_earnings"
    othertotal_stockholders_equity_field = ""
    total_stockholders_equity_field = "total_equity_gross_minority_interest"
    total_liabilities_and_total_equity_field = "total_assets"
    total_investments_field = ""
    total_debt_field = "total_debt"
    net_debt_field = "net_debt"


class CashflowStatementYahooQueryExtended(NormalizeCashflowStatement):
    net_income_field = "net_income"
    depreciation_amortization_field = "depreciation_and_amortization"
    deferred_income_tax_field = "deferred_income_tax"
    stock_based_compensation_field = "stock_based_compensation"
    change_in_working_capital_field = "change_in_working_capital"
    accounts_receivable_field = "changes_in_account_receivables"
    inventory_field = "change_in_inventory"
    accounts_payable_field = ""
    other_working_capital_field = "change_in_other_working_capital"
    other_non_cash_items_field = "other_non_cash_items"
    operating_activities_cf_field = "cash_flow_from_continuing_operating_activities"
    investments_property_plant_equipment_field = ""
    acquisitions_net_field = "purchase_of_business"
    purchases_investments_field = "purchase_of_investment"
    sales_maturities_investments_field = "sale_of_investment"
    other_investing_activites_field = "net_other_investing_changes"
    investing_activities_cf_field = "cash_flow_from_continuing_investing_activities"
    debt_repayment_field = "repayment_of_debt"
    common_stock_issued_field = "issuance_of_capital_stock"
    common_stock_repurchased_field = "repurchase_of_capital_stock"
    dividends_paid_field = "common_stock_dividend_paid"
    other_financing_activities_field = "net_other_financing_charges"
    financing_activities_cf_field = "cash_flow_from_continuing_financing_activities"
    effect_forex_exchange_field = ""
    net_change_cash_field = ""
    cash_end_period_field = "end_cash_position"
    cash_beginning_period_field = "beginning_cash_position"
    operating_cf_field = "operating_cash_flow"
    capex_field = "capital_expenditure"
    fcf_field = "free_cash_flow"
