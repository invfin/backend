from typing import Dict, Optional, Union


class BaseNormalizeStatement:
    reported_currency_id_field: str = "reported_currency_id"

    def get_reported_currency(self) -> Optional[Union[int, float]]:
        return getattr(self, self.reported_currency_id_field, None)

    def return_standard(self) -> Dict[str, Optional[Union[int, float]]]:
        return dict(
            reported_currency_id=self.get_reported_currency(),
        )


class NormalizeIncomeStatement(BaseNormalizeStatement):
    revenue_field: str = "revenue"
    cost_of_revenue_field: str = "cost_of_revenue"
    gross_profit_field: str = "gross_profit"
    rd_expenses_field: str = "rd_expenses"
    general_administrative_expenses_field: str = "general_administrative_expenses"
    selling_marketing_expenses_field: str = "selling_marketing_expenses"
    sga_expenses_field: str = "sga_expenses"
    other_expenses_field: str = "other_expenses"
    operating_expenses_field: str = "operating_expenses"
    cost_and_expenses_field: str = "cost_and_expenses"
    interest_expense_field: str = "interest_expense"
    depreciation_amortization_field: str = "depreciation_amortization"
    ebitda_field: str = "ebitda"
    operating_income_field: str = "operating_income"
    net_total_other_income_expenses_field: str = "net_total_other_income_expenses"
    income_before_tax_field: str = "income_before_tax"
    income_tax_expenses_field: str = "income_tax_expenses"
    net_income_field: str = "net_income"
    weighted_average_shares_outstanding_field: str = "weighted_average_shares_outstanding"
    weighted_average_diluated_shares_outstanding_field: str = (
        "weighted_average_diluated_shares_outstanding"
    )

    def return_standard(self) -> Dict[str, Optional[Union[int, float]]]:
        return dict(
            **super().return_standard(),
            revenue=self.get_revenue(),
            cost_of_revenue=self.get_cost_of_revenue(),
            gross_profit=self.get_gross_profit(),
            rd_expenses=self.get_rd_expenses(),
            general_administrative_expenses=self.get_general_administrative_expenses(),
            selling_marketing_expenses=self.get_selling_marketing_expenses(),
            sga_expenses=self.get_sga_expenses(),
            other_expenses=self.get_other_expenses(),
            operating_expenses=self.get_operating_expenses(),
            cost_and_expenses=self.get_cost_and_expenses(),
            interest_expense=self.get_interest_expense(),
            depreciation_amortization=self.get_depreciation_amortization(),
            ebitda=self.get_ebitda(),
            operating_income=self.get_operating_income(),
            net_total_other_income_expenses=self.get_net_total_other_income_expenses(),
            income_before_tax=self.get_income_before_tax(),
            income_tax_expenses=self.get_income_tax_expenses(),
            net_income=self.get_net_income(),
            weighted_average_shares_outstanding=self.get_weighted_average_shares_outstanding(),
            weighted_average_diluated_shares_outstanding=self.get_weighted_average_diluated_shares_outstanding(),
        )

    def get_revenue(self) -> Optional[Union[int, float]]:
        return getattr(self, self.revenue_field, None)

    def get_cost_of_revenue(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cost_of_revenue_field, None)

    def get_gross_profit(self) -> Optional[Union[int, float]]:
        return getattr(self, self.gross_profit_field, None)

    def get_rd_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.rd_expenses_field, None)

    def get_general_administrative_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.general_administrative_expenses_field, None)

    def get_selling_marketing_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.selling_marketing_expenses_field, None)

    def get_sga_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.sga_expenses_field, None)

    def get_other_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_expenses_field, None)

    def get_operating_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.operating_expenses_field, None)

    def get_cost_and_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cost_and_expenses_field, None)

    def get_interest_expense(self) -> Optional[Union[int, float]]:
        return getattr(self, self.interest_expense_field, None)

    def get_depreciation_amortization(self) -> Optional[Union[int, float]]:
        return getattr(self, self.depreciation_amortization_field, None)

    def get_ebitda(self) -> Optional[Union[int, float]]:
        return getattr(self, self.ebitda_field, None)

    def get_operating_income(self) -> Optional[Union[int, float]]:
        return getattr(self, self.operating_income_field, None)

    def get_net_total_other_income_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_total_other_income_expenses_field, None)

    def get_income_before_tax(self) -> Optional[Union[int, float]]:
        return getattr(self, self.income_before_tax_field, None)

    def get_income_tax_expenses(self) -> Optional[Union[int, float]]:
        return getattr(self, self.income_tax_expenses_field, None)

    def get_net_income(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_income_field, None)

    def get_weighted_average_shares_outstanding(self) -> Optional[Union[int, float]]:
        return getattr(self, self.weighted_average_shares_outstanding_field, None)

    def get_weighted_average_diluated_shares_outstanding(self) -> Optional[Union[int, float]]:
        return getattr(self, self.weighted_average_diluated_shares_outstanding_field, None)


class NormalizeBalanceSheet(BaseNormalizeStatement):
    cash_and_cash_equivalents_field: str = "cash_and_cash_equivalents"
    short_term_investments_field: str = "short_term_investments"
    cash_and_short_term_investments_field: str = "cash_and_short_term_investments"
    net_receivables_field: str = "net_receivables"
    inventory_field: str = "inventory"
    other_current_assets_field: str = "other_current_assets"
    total_current_assets_field: str = "total_current_assets"
    property_plant_equipment_field: str = "property_plant_equipment"
    goodwill_field: str = "goodwill"
    intangible_assets_field: str = "intangible_assets"
    goodwill_and_intangible_assets_field: str = "goodwill_and_intangible_assets"
    long_term_investments_field: str = "long_term_investments"
    tax_assets_field: str = "tax_assets"
    other_non_current_assets_field: str = "other_non_current_assets"
    total_non_current_assets_field: str = "total_non_current_assets"
    other_assets_field: str = "other_assets"
    total_assets_field: str = "total_assets"
    accounts_payable_field: str = "accounts_payable"
    short_term_debt_field: str = "short_term_debt"
    tax_payables_field: str = "tax_payables"
    deferred_revenue_field: str = "deferred_revenue"
    other_current_liabilities_field: str = "other_current_liabilities"
    total_current_liabilities_field: str = "total_current_liabilities"
    long_term_debt_field: str = "long_term_debt"
    deferred_revenue_non_current_field: str = "deferred_revenue_non_current"
    deferred_tax_liabilities_non_current_field: str = "deferred_tax_liabilities_non_current"
    other_non_current_liabilities_field: str = "other_non_current_liabilities"
    total_non_current_liabilities_field: str = "total_non_current_liabilities"
    other_liabilities_field: str = "other_liabilities"
    total_liabilities_field: str = "total_liabilities"
    common_stocks_field: str = "common_stocks"
    retained_earnings_field: str = "retained_earnings"
    accumulated_other_comprehensive_income_loss_field: str = (
        "accumulated_other_comprehensive_income_loss"
    )
    othertotal_stockholders_equity_field: str = "othertotal_stockholders_equity"
    total_stockholders_equity_field: str = "total_stockholders_equity"
    total_liabilities_and_total_equity_field: str = "total_liabilities_and_total_equity"
    total_investments_field: str = "total_investments"
    total_debt_field: str = "total_debt"
    net_debt_field: str = "net_debt"

    def return_standard(self) -> Dict[str, Optional[Union[int, float]]]:
        return dict(
            **super().return_standard(),
            cash_and_cash_equivalents=self.get_cash_and_cash_equivalents(),
            short_term_investments=self.get_short_term_investments(),
            cash_and_short_term_investments=self.get_cash_and_short_term_investments(),
            net_receivables=self.get_net_receivables(),
            inventory=self.get_inventory(),
            other_current_assets=self.get_other_current_assets(),
            total_current_assets=self.get_total_current_assets(),
            property_plant_equipment=self.get_property_plant_equipment(),
            goodwill=self.get_goodwill(),
            intangible_assets=self.get_intangible_assets(),
            goodwill_and_intangible_assets=self.get_goodwill_and_intangible_assets(),
            long_term_investments=self.get_long_term_investments(),
            tax_assets=self.get_tax_assets(),
            other_non_current_assets=self.get_other_non_current_assets(),
            total_non_current_assets=self.get_total_non_current_assets(),
            other_assets=self.get_other_assets(),
            total_assets=self.get_total_assets(),
            accounts_payable=self.get_accounts_payable(),
            short_term_debt=self.get_short_term_debt(),
            tax_payables=self.get_tax_payables(),
            deferred_revenue=self.get_deferred_revenue(),
            other_current_liabilities=self.get_other_current_liabilities(),
            total_current_liabilities=self.get_total_current_liabilities(),
            long_term_debt=self.get_long_term_debt(),
            deferred_revenue_non_current=self.get_deferred_revenue_non_current(),
            deferred_tax_liabilities_non_current=self.get_deferred_tax_liabilities_non_current(),
            other_non_current_liabilities=self.get_other_non_current_liabilities(),
            total_non_current_liabilities=self.get_total_non_current_liabilities(),
            other_liabilities=self.get_other_liabilities(),
            total_liabilities=self.get_total_liabilities(),
            common_stocks=self.get_common_stocks(),
            retained_earnings=self.get_retained_earnings(),
            accumulated_other_comprehensive_income_loss=self.get_accumulated_other_comprehensive_income_loss(),
            othertotal_stockholders_equity=self.get_othertotal_stockholders_equity(),
            total_stockholders_equity=self.get_total_stockholders_equity(),
            total_liabilities_and_total_equity=self.get_total_liabilities_and_total_equity(),
            total_investments=self.get_total_investments(),
            total_debt=self.get_total_debt(),
            net_debt=self.get_net_debt(),
        )

    def get_cash_and_cash_equivalents(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cash_and_cash_equivalents_field, None)

    def get_short_term_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.short_term_investments_field, None)

    def get_cash_and_short_term_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cash_and_short_term_investments_field, None)

    def get_net_receivables(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_receivables_field, None)

    def get_inventory(self) -> Optional[Union[int, float]]:
        return getattr(self, self.inventory_field, None)

    def get_other_current_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_current_assets_field, None)

    def get_total_current_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_current_assets_field, None)

    def get_property_plant_equipment(self) -> Optional[Union[int, float]]:
        return getattr(self, self.property_plant_equipment_field, None)

    def get_goodwill(self) -> Optional[Union[int, float]]:
        return getattr(self, self.goodwill_field, None)

    def get_intangible_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.intangible_assets_field, None)

    def get_goodwill_and_intangible_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.goodwill_and_intangible_assets_field, None)

    def get_long_term_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.long_term_investments_field, None)

    def get_tax_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.tax_assets_field, None)

    def get_other_non_current_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_non_current_assets_field, None)

    def get_total_non_current_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_non_current_assets_field, None)

    def get_other_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_assets_field, None)

    def get_total_assets(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_assets_field, None)

    def get_accounts_payable(self) -> Optional[Union[int, float]]:
        return getattr(self, self.accounts_payable_field, None)

    def get_short_term_debt(self) -> Optional[Union[int, float]]:
        return getattr(self, self.short_term_debt_field, None)

    def get_tax_payables(self) -> Optional[Union[int, float]]:
        return getattr(self, self.tax_payables_field, None)

    def get_deferred_revenue(self) -> Optional[Union[int, float]]:
        return getattr(self, self.deferred_revenue_field, None)

    def get_other_current_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_current_liabilities_field, None)

    def get_total_current_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_current_liabilities_field, None)

    def get_long_term_debt(self) -> Optional[Union[int, float]]:
        return getattr(self, self.long_term_debt_field, None)

    def get_deferred_revenue_non_current(self) -> Optional[Union[int, float]]:
        return getattr(self, self.deferred_revenue_non_current_field, None)

    def get_deferred_tax_liabilities_non_current(self) -> Optional[Union[int, float]]:
        return getattr(self, self.deferred_tax_liabilities_non_current_field, None)

    def get_other_non_current_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_non_current_liabilities_field, None)

    def get_total_non_current_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_non_current_liabilities_field, None)

    def get_other_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_liabilities_field, None)

    def get_total_liabilities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_liabilities_field, None)

    def get_common_stocks(self) -> Optional[Union[int, float]]:
        return getattr(self, self.common_stocks_field, None)

    def get_retained_earnings(self) -> Optional[Union[int, float]]:
        return getattr(self, self.retained_earnings_field, None)

    def get_accumulated_other_comprehensive_income_loss(self) -> Optional[Union[int, float]]:
        return getattr(self, self.accumulated_other_comprehensive_income_loss_field, None)

    def get_othertotal_stockholders_equity(self) -> Optional[Union[int, float]]:
        return getattr(self, self.othertotal_stockholders_equity_field, None)

    def get_total_stockholders_equity(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_stockholders_equity_field, None)

    def get_total_liabilities_and_total_equity(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_liabilities_and_total_equity_field, None)

    def get_total_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_investments_field, None)

    def get_total_debt(self) -> Optional[Union[int, float]]:
        return getattr(self, self.total_debt_field, None)

    def get_net_debt(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_debt_field, None)


class NormalizeCashflowStatement(BaseNormalizeStatement):
    net_income_field: str = "net_income"
    depreciation_amortization_field: str = "depreciation_amortization"
    deferred_income_tax_field: str = "deferred_income_tax"
    stock_based_compensation_field: str = "stock_based_compensation"
    change_in_working_capital_field: str = "change_in_working_capital"
    accounts_receivable_field: str = "accounts_receivable"
    inventory_field: str = "inventory"
    accounts_payable_field: str = "accounts_payable"
    other_working_capital_field: str = "other_working_capital"
    other_non_cash_items_field: str = "other_non_cash_items"
    operating_activities_cf_field: str = "operating_activities_cf"
    investments_property_plant_equipment_field: str = "investments_property_plant_equipment"
    acquisitions_net_field: str = "acquisitions_net"
    purchases_investments_field: str = "purchases_investments"
    sales_maturities_investments_field: str = "sales_maturities_investments"
    other_investing_activites_field: str = "other_investing_activites"
    investing_activities_cf_field: str = "investing_activities_cf"
    debt_repayment_field: str = "debt_repayment"
    common_stock_issued_field: str = "common_stock_issued"
    common_stock_repurchased_field: str = "common_stock_repurchased"
    dividends_paid_field: str = "dividends_paid"
    other_financing_activities_field: str = "other_financing_activities"
    financing_activities_cf_field: str = "financing_activities_cf"
    effect_forex_exchange_field: str = "effect_forex_exchange"
    net_change_cash_field: str = "net_change_cash"
    cash_end_period_field: str = "cash_end_period"
    cash_beginning_period_field: str = "cash_beginning_period"
    operating_cf_field: str = "operating_cf"
    capex_field: str = "capex"
    fcf_field: str = "fcf"

    def return_standard(self) -> Dict[str, Optional[Union[int, float]]]:
        return dict(
            **super().return_standard(),
            net_income=self.get_net_income(),
            depreciation_amortization=self.get_depreciation_amortization(),
            deferred_income_tax=self.get_deferred_income_tax(),
            stock_based_compensation=self.get_stock_based_compensation(),
            change_in_working_capital=self.get_change_in_working_capital(),
            accounts_receivable=self.get_accounts_receivable(),
            inventory=self.get_inventory(),
            accounts_payable=self.get_accounts_payable(),
            other_working_capital=self.get_other_working_capital(),
            other_non_cash_items=self.get_other_non_cash_items(),
            operating_activities_cf=self.get_operating_activities_cf(),
            investments_property_plant_equipment=self.get_investments_property_plant_equipment(),
            acquisitions_net=self.get_acquisitions_net(),
            purchases_investments=self.get_purchases_investments(),
            sales_maturities_investments=self.get_sales_maturities_investments(),
            other_investing_activites=self.get_other_investing_activites(),
            investing_activities_cf=self.get_investing_activities_cf(),
            debt_repayment=self.get_debt_repayment(),
            common_stock_issued=self.get_common_stock_issued(),
            common_stock_repurchased=self.get_common_stock_repurchased(),
            dividends_paid=self.get_dividends_paid(),
            other_financing_activities=self.get_other_financing_activities(),
            financing_activities_cf=self.get_financing_activities_cf(),
            effect_forex_exchange=self.get_effect_forex_exchange(),
            net_change_cash=self.get_net_change_cash(),
            cash_end_period=self.get_cash_end_period(),
            cash_beginning_period=self.get_cash_beginning_period(),
            operating_cf=self.get_operating_cf(),
            capex=self.get_capex(),
            fcf=self.get_fcf(),
        )

    def get_net_income(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_income_field, None)

    def get_depreciation_amortization(self) -> Optional[Union[int, float]]:
        return getattr(self, self.depreciation_amortization_field, None)

    def get_deferred_income_tax(self) -> Optional[Union[int, float]]:
        return getattr(self, self.deferred_income_tax_field, None)

    def get_stock_based_compensation(self) -> Optional[Union[int, float]]:
        return getattr(self, self.stock_based_compensation_field, None)

    def get_change_in_working_capital(self) -> Optional[Union[int, float]]:
        return getattr(self, self.change_in_working_capital_field, None)

    def get_accounts_receivable(self) -> Optional[Union[int, float]]:
        return getattr(self, self.accounts_receivable_field, None)

    def get_inventory(self) -> Optional[Union[int, float]]:
        return getattr(self, self.inventory_field, None)

    def get_accounts_payable(self) -> Optional[Union[int, float]]:
        return getattr(self, self.accounts_payable_field, None)

    def get_other_working_capital(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_working_capital_field, None)

    def get_other_non_cash_items(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_non_cash_items_field, None)

    def get_operating_activities_cf(self) -> Optional[Union[int, float]]:
        return getattr(self, self.operating_activities_cf_field, None)

    def get_investments_property_plant_equipment(self) -> Optional[Union[int, float]]:
        return getattr(self, self.investments_property_plant_equipment_field, None)

    def get_acquisitions_net(self) -> Optional[Union[int, float]]:
        return getattr(self, self.acquisitions_net_field, None)

    def get_purchases_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.purchases_investments_field, None)

    def get_sales_maturities_investments(self) -> Optional[Union[int, float]]:
        return getattr(self, self.sales_maturities_investments_field, None)

    def get_other_investing_activites(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_investing_activites_field, None)

    def get_investing_activities_cf(self) -> Optional[Union[int, float]]:
        return getattr(self, self.investing_activities_cf_field, None)

    def get_debt_repayment(self) -> Optional[Union[int, float]]:
        return getattr(self, self.debt_repayment_field, None)

    def get_common_stock_issued(self) -> Optional[Union[int, float]]:
        return getattr(self, self.common_stock_issued_field, None)

    def get_common_stock_repurchased(self) -> Optional[Union[int, float]]:
        return getattr(self, self.common_stock_repurchased_field, None)

    def get_dividends_paid(self) -> Optional[Union[int, float]]:
        return getattr(self, self.dividends_paid_field, None)

    def get_other_financing_activities(self) -> Optional[Union[int, float]]:
        return getattr(self, self.other_financing_activities_field, None)

    def get_financing_activities_cf(self) -> Optional[Union[int, float]]:
        return getattr(self, self.financing_activities_cf_field, None)

    def get_effect_forex_exchange(self) -> Optional[Union[int, float]]:
        return getattr(self, self.effect_forex_exchange_field, None)

    def get_net_change_cash(self) -> Optional[Union[int, float]]:
        return getattr(self, self.net_change_cash_field, None)

    def get_cash_end_period(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cash_end_period_field, None)

    def get_cash_beginning_period(self) -> Optional[Union[int, float]]:
        return getattr(self, self.cash_beginning_period_field, None)

    def get_operating_cf(self) -> Optional[Union[int, float]]:
        return getattr(self, self.operating_cf_field, None)

    def get_capex(self) -> Optional[Union[int, float]]:
        return getattr(self, self.capex_field, None)

    def get_fcf(self) -> Optional[Union[int, float]]:
        return getattr(self, self.fcf_field, None)
