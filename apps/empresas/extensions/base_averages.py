class AverageIncomeStatement:
    revenue_field: str = None
    cost_of_revenue_field: str = None
    gross_profit_field: str = None
    rd_expenses_field: str = None
    general_administrative_expenses_field: str = None
    selling_marketing_expenses_field: str = None
    sga_expenses_field: str = None
    other_expenses_field: str = None
    operating_expenses_field: str = None
    cost_and_expenses_field: str = None
    interest_expense_field: str = None
    depreciation_amortization_field: str = None
    ebitda_field: str = None
    operating_income_field: str = None
    net_total_other_income_expenses_field: str = None
    income_before_tax_field: str = None
    income_tax_expenses_field: str = None
    net_income_field: str = None
    weighted_average_shares_outstanding_field: str = None
    weighted_average_diluated_shares_outstanding_field: str = None

    def calculate_revenue(self):
        return getattr(self, self.revenue_field)

    def calculate_cost_of_revenue(self):
        return getattr(self, self.cost_of_revenue_field)

    def calculate_gross_profit(self):
        return getattr(self, self.gross_profit_field)

    def calculate_rd_expenses(self):
        return getattr(self, self.rd_expenses_field)

    def calculate_general_administrative_expenses(self):
        return getattr(self, self.general_administrative_expenses_field)

    def calculate_selling_marketing_expenses(self):
        return getattr(self, self.selling_marketing_expenses_field)

    def calculate_sga_expenses(self):
        return getattr(self, self.sga_expenses_field)

    def calculate_other_expenses(self):
        return getattr(self, self.other_expenses_field)

    def calculate_operating_expenses(self):
        return getattr(self, self.operating_expenses_field)

    def calculate_cost_and_expenses(self):
        return getattr(self, self.cost_and_expenses_field)

    def calculate_interest_expense(self):
        return getattr(self, self.interest_expense_field)

    def calculate_depreciation_amortization(self):
        return getattr(self, self.depreciation_amortization_field)

    def calculate_ebitda(self):
        return getattr(self, self.ebitda_field)

    def calculate_operating_income(self):
        return getattr(self, self.operating_income_field)

    def calculate_net_total_other_income_expenses(self):
        return getattr(self, self.net_total_other_income_expenses_field)

    def calculate_income_before_tax(self):
        return getattr(self, self.income_before_tax_field)

    def calculate_income_tax_expenses(self):
        return getattr(self, self.income_tax_expenses_field)

    def calculate_net_income(self):
        return getattr(self, self.net_income_field)

    def calculate_weighted_average_shares_outstanding(self):
        return getattr(self, self.weighted_average_shares_outstanding_field)

    def calculate_weighted_average_diluated_shares_outstanding(self):
        return getattr(self, self.weighted_average_diluated_shares_outstanding_field)

    def return_standard(self):
        return dict(
            revenue=self.calculate_revenue(),
            cost_of_revenue=self.calculate_cost_of_revenue(),
            gross_profit=self.calculate_gross_profit(),
            rd_expenses=self.calculate_rd_expenses(),
            general_administrative_expenses=self.calculate_general_administrative_expenses(),
            selling_marketing_expenses=self.calculate_selling_marketing_expenses(),
            sga_expenses=self.calculate_sga_expenses(),
            other_expenses=self.calculate_other_expenses(),
            operating_expenses=self.calculate_operating_expenses(),
            cost_and_expenses=self.calculate_cost_and_expenses(),
            interest_expense=self.calculate_interest_expense(),
            depreciation_amortization=self.calculate_depreciation_amortization(),
            ebitda=self.calculate_ebitda(),
            operating_income=self.calculate_operating_income(),
            net_total_other_income_expenses=self.calculate_net_total_other_income_expenses(),
            income_before_tax=self.calculate_income_before_tax(),
            income_tax_expenses=self.calculate_income_tax_expenses(),
            net_income=self.calculate_net_income(),
            weighted_average_shares_outstanding=self.calculate_weighted_average_shares_outstanding(),
            weighted_average_diluated_shares_outstanding=self.calculate_weighted_average_diluated_shares_outstanding(),
        )


class AverageBalanceSheet:
    cash_and_cash_equivalents_field: str = None
    short_term_investments_field: str = None
    cash_and_short_term_investments_field: str = None
    net_receivables_field: str = None
    inventory_field: str = None
    other_current_assets_field: str = None
    total_current_assets_field: str = None
    property_plant_equipment_field: str = None
    goodwill_field: str = None
    intangible_assets_field: str = None
    goodwill_and_intangible_assets_field: str = None
    long_term_investments_field: str = None
    tax_assets_field: str = None
    other_non_current_assets_field: str = None
    total_non_current_assets_field: str = None
    other_assets_field: str = None
    total_assets_field: str = None
    account_payables_field: str = None
    short_term_debt_field: str = None
    tax_payables_field: str = None
    deferred_revenue_field: str = None
    other_current_liabilities_field: str = None
    total_current_liabilities_field: str = None
    long_term_debt_field: str = None
    deferred_revenue_non_current_field: str = None
    deferred_tax_liabilities_non_current_field: str = None
    other_non_current_liabilities_field: str = None
    total_non_current_liabilities_field: str = None
    other_liabilities_field: str = None
    total_liabilities_field: str = None
    common_stocks_field: str = None
    retained_earnings_field: str = None
    accumulated_other_comprehensive_income_loss_field: str = None
    othertotal_stockholders_equity_field: str = None
    total_stockholders_equity_field: str = None
    total_liabilities_and_total_equity_field: str = None
    total_investments_field: str = None
    total_debt_field: str = None
    net_debt_field: str = None

    def calculate_cash_and_cash_equivalents(self):
        return getattr(self, self.cash_and_cash_equivalents_field)

    def calculate_short_term_investments(self):
        return getattr(self, self.short_term_investments_field)

    def calculate_cash_and_short_term_investments(self):
        return getattr(self, self.cash_and_short_term_investments_field)

    def calculate_net_receivables(self):
        return getattr(self, self.net_receivables_field)

    def calculate_inventory(self):
        return getattr(self, self.inventory_field)

    def calculate_other_current_assets(self):
        return getattr(self, self.other_current_assets_field)

    def calculate_total_current_assets(self):
        return getattr(self, self.total_current_assets_field)

    def calculate_property_plant_equipment(self):
        return getattr(self, self.property_plant_equipment_field)

    def calculate_goodwill(self):
        return getattr(self, self.goodwill_field)

    def calculate_intangible_assets(self):
        return getattr(self, self.intangible_assets_field)

    def calculate_goodwill_and_intangible_assets(self):
        return getattr(self, self.goodwill_and_intangible_assets_field)

    def calculate_long_term_investments(self):
        return getattr(self, self.long_term_investments_field)

    def calculate_tax_assets(self):
        return getattr(self, self.tax_assets_field)

    def calculate_other_non_current_assets(self):
        return getattr(self, self.other_non_current_assets_field)

    def calculate_total_non_current_assets(self):
        return getattr(self, self.total_non_current_assets_field)

    def calculate_other_assets(self):
        return getattr(self, self.other_assets_field)

    def calculate_total_assets(self):
        return getattr(self, self.total_assets_field)

    def calculate_account_payables(self):
        return getattr(self, self.account_payables_field)

    def calculate_short_term_debt(self):
        return getattr(self, self.short_term_debt_field)

    def calculate_tax_payables(self):
        return getattr(self, self.tax_payables_field)

    def calculate_deferred_revenue(self):
        return getattr(self, self.deferred_revenue_field)

    def calculate_other_current_liabilities(self):
        return getattr(self, self.other_current_liabilities_field)

    def calculate_total_current_liabilities(self):
        return getattr(self, self.total_current_liabilities_field)

    def calculate_long_term_debt(self):
        return getattr(self, self.long_term_debt_field)

    def calculate_deferred_revenue_non_current(self):
        return getattr(self, self.deferred_revenue_non_current_field)

    def calculate_deferred_tax_liabilities_non_current(self):
        return getattr(self, self.deferred_tax_liabilities_non_current_field)

    def calculate_other_non_current_liabilities(self):
        return getattr(self, self.other_non_current_liabilities_field)

    def calculate_total_non_current_liabilities(self):
        return getattr(self, self.total_non_current_liabilities_field)

    def calculate_other_liabilities(self):
        return getattr(self, self.other_liabilities_field)

    def calculate_total_liabilities(self):
        return getattr(self, self.total_liabilities_field)

    def calculate_common_stocks(self):
        return getattr(self, self.common_stocks_field)

    def calculate_retained_earnings(self):
        return getattr(self, self.retained_earnings_field)

    def calculate_accumulated_other_comprehensive_income_loss(self):
        return getattr(self, self.accumulated_other_comprehensive_income_loss_field)

    def calculate_othertotal_stockholders_equity(self):
        return getattr(self, self.othertotal_stockholders_equity_field)

    def calculate_total_stockholders_equity(self):
        return getattr(self, self.total_stockholders_equity_field)

    def calculate_total_liabilities_and_total_equity(self):
        return getattr(self, self.total_liabilities_and_total_equity_field)

    def calculate_total_investments(self):
        return getattr(self, self.total_investments_field)

    def calculate_total_debt(self):
        return getattr(self, self.total_debt_field)

    def calculate_net_debt(self):
        return getattr(self, self.net_debt_field)

    def return_standard(self):
        return dict(
            cash_and_cash_equivalents=self.calculate_cash_and_cash_equivalents(),
            short_term_investments=self.calculate_short_term_investments(),
            cash_and_short_term_investments=self.calculate_cash_and_short_term_investments(),
            net_receivables=self.calculate_net_receivables(),
            inventory=self.calculate_inventory(),
            other_current_assets=self.calculate_other_current_assets(),
            total_current_assets=self.calculate_total_current_assets(),
            property_plant_equipment=self.calculate_property_plant_equipment(),
            goodwill=self.calculate_goodwill(),
            intangible_assets=self.calculate_intangible_assets(),
            goodwill_and_intangible_assets=self.calculate_goodwill_and_intangible_assets(),
            long_term_investments=self.calculate_long_term_investments(),
            tax_assets=self.calculate_tax_assets(),
            other_non_current_assets=self.calculate_other_non_current_assets(),
            total_non_current_assets=self.calculate_total_non_current_assets(),
            other_assets=self.calculate_other_assets(),
            total_assets=self.calculate_total_assets(),
            account_payables=self.calculate_account_payables(),
            short_term_debt=self.calculate_short_term_debt(),
            tax_payables=self.calculate_tax_payables(),
            deferred_revenue=self.calculate_deferred_revenue(),
            other_current_liabilities=self.calculate_other_current_liabilities(),
            total_current_liabilities=self.calculate_total_current_liabilities(),
            long_term_debt=self.calculate_long_term_debt(),
            deferred_revenue_non_current=self.calculate_deferred_revenue_non_current(),
            deferred_tax_liabilities_non_current=self.calculate_deferred_tax_liabilities_non_current(),
            other_non_current_liabilities=self.calculate_other_non_current_liabilities(),
            total_non_current_liabilities=self.calculate_total_non_current_liabilities(),
            other_liabilities=self.calculate_other_liabilities(),
            total_liabilities=self.calculate_total_liabilities(),
            common_stocks=self.calculate_common_stocks(),
            retained_earnings=self.calculate_retained_earnings(),
            accumulated_other_comprehensive_income_loss=self.calculate_accumulated_other_comprehensive_income_loss(),
            othertotal_stockholders_equity=self.calculate_othertotal_stockholders_equity(),
            total_stockholders_equity=self.calculate_total_stockholders_equity(),
            total_liabilities_and_total_equity=self.calculate_total_liabilities_and_total_equity(),
            total_investments=self.calculate_total_investments(),
            total_debt=self.calculate_total_debt(),
            net_debt=self.calculate_net_debt(),
        )


class AverageCashflowStatement:
    net_income_field: str = None
    depreciation_amortization_field: str = None
    deferred_income_tax_field: str = None
    stock_based_compesation_field: str = None
    change_in_working_capital_field: str = None
    accounts_receivables_field: str = None
    inventory_field: str = None
    accounts_payable_field: str = None
    other_working_capital_field: str = None
    other_non_cash_items_field: str = None
    operating_activities_cf_field: str = None
    investments_property_plant_equipment_field: str = None
    acquisitions_net_field: str = None
    purchases_investments_field: str = None
    sales_maturities_investments_field: str = None
    other_investing_activites_field: str = None
    investing_activities_cf_field: str = None
    debt_repayment_field: str = None
    common_stock_issued_field: str = None
    common_stock_repurchased_field: str = None
    dividends_paid_field: str = None
    other_financing_activities_field: str = None
    financing_activities_cf_field: str = None
    effect_forex_exchange_field: str = None
    net_change_cash_field: str = None
    cash_end_period_field: str = None
    cash_beginning_period_field: str = None
    operating_cf_field: str = None
    capex_field: str = None
    fcf_field: str = None

    def calculate_net_income(self):
        return getattr(self, self.net_income_field)

    def calculate_depreciation_amortization(self):
        return getattr(self, self.depreciation_amortization_field)

    def calculate_deferred_income_tax(self):
        return getattr(self, self.deferred_income_tax_field)

    def calculate_stock_based_compesation(self):
        return getattr(self, self.stock_based_compesation_field)

    def calculate_change_in_working_capital(self):
        return getattr(self, self.change_in_working_capital_field)

    def calculate_accounts_receivables(self):
        return getattr(self, self.accounts_receivables_field)

    def calculate_inventory(self):
        return getattr(self, self.inventory_field)

    def calculate_accounts_payable(self):
        return getattr(self, self.accounts_payable_field)

    def calculate_other_working_capital(self):
        return getattr(self, self.other_working_capital_field)

    def calculate_other_non_cash_items(self):
        return getattr(self, self.other_non_cash_items_field)

    def calculate_operating_activities_cf(self):
        return getattr(self, self.operating_activities_cf_field)

    def calculate_investments_property_plant_equipment(self):
        return getattr(self, self.investments_property_plant_equipment_field)

    def calculate_acquisitions_net(self):
        return getattr(self, self.acquisitions_net_field)

    def calculate_purchases_investments(self):
        return getattr(self, self.purchases_investments_field)

    def calculate_sales_maturities_investments(self):
        return getattr(self, self.sales_maturities_investments_field)

    def calculate_other_investing_activites(self):
        return getattr(self, self.other_investing_activites_field)

    def calculate_investing_activities_cf(self):
        return getattr(self, self.investing_activities_cf_field)

    def calculate_debt_repayment(self):
        return getattr(self, self.debt_repayment_field)

    def calculate_common_stock_issued(self):
        return getattr(self, self.common_stock_issued_field)

    def calculate_common_stock_repurchased(self):
        return getattr(self, self.common_stock_repurchased_field)

    def calculate_dividends_paid(self):
        return getattr(self, self.dividends_paid_field)

    def calculate_other_financing_activities(self):
        return getattr(self, self.other_financing_activities_field)

    def calculate_financing_activities_cf(self):
        return getattr(self, self.financing_activities_cf_field)

    def calculate_effect_forex_exchange(self):
        return getattr(self, self.effect_forex_exchange_field)

    def calculate_net_change_cash(self):
        return getattr(self, self.net_change_cash_field)

    def calculate_cash_end_period(self):
        return getattr(self, self.cash_end_period_field)

    def calculate_cash_beginning_period(self):
        return getattr(self, self.cash_beginning_period_field)

    def calculate_operating_cf(self):
        return getattr(self, self.operating_cf_field)

    def calculate_capex(self):
        return getattr(self, self.capex_field)

    def calculate_fcf(self):
        return getattr(self, self.fcf_field)

    def return_standard(self):
        return dict(
            net_income=self.calculate_net_income(),
            depreciation_amortization=self.calculate_depreciation_amortization(),
            deferred_income_tax=self.calculate_deferred_income_tax(),
            stock_based_compesation=self.calculate_stock_based_compesation(),
            change_in_working_capital=self.calculate_change_in_working_capital(),
            accounts_receivables=self.calculate_accounts_receivables(),
            inventory=self.calculate_inventory(),
            accounts_payable=self.calculate_accounts_payable(),
            other_working_capital=self.calculate_other_working_capital(),
            other_non_cash_items=self.calculate_other_non_cash_items(),
            operating_activities_cf=self.calculate_operating_activities_cf(),
            investments_property_plant_equipment=self.calculate_investments_property_plant_equipment(),
            acquisitions_net=self.calculate_acquisitions_net(),
            purchases_investments=self.calculate_purchases_investments(),
            sales_maturities_investments=self.calculate_sales_maturities_investments(),
            other_investing_activites=self.calculate_other_investing_activites(),
            investing_activities_cf=self.calculate_investing_activities_cf(),
            debt_repayment=self.calculate_debt_repayment(),
            common_stock_issued=self.calculate_common_stock_issued(),
            common_stock_repurchased=self.calculate_common_stock_repurchased(),
            dividends_paid=self.calculate_dividends_paid(),
            other_financing_activities=self.calculate_other_financing_activities(),
            financing_activities_cf=self.calculate_financing_activities_cf(),
            effect_forex_exchange=self.calculate_effect_forex_exchange(),
            net_change_cash=self.calculate_net_change_cash(),
            cash_end_period=self.calculate_cash_end_period(),
            cash_beginning_period=self.calculate_cash_beginning_period(),
            operating_cf=self.calculate_operating_cf(),
            capex=self.calculate_capex(),
            fcf=self.calculate_fcf(),
        )
