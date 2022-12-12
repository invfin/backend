from src.empresas.outils.financial_ratios import CalculateFinancialRatios


class TestCalculateFinancialRatios:
    def test_generate_current_data(self):
        data = {}
        expected_data = {}
        assert expected_data == CalculateFinancialRatios.generate_current_data(data)

    def test_generate_last_year_data(self):
        data = {}
        expected_data = {}
        assert expected_data == CalculateFinancialRatios.generate_last_year_data(data)

    def test_calculate_all_ratios(self):
        data = {}
        expected_data = {
            "current_data": 0,
            "price_to_ratio": 0,
            "efficiency_ratio": 0,
            "enterprise_value_ratio": 0,
            "liquidity_ratio": 0,
            "margin_ratio": 0,
            "operation_risk_ratio": 0,
            "rentability_ratios": 0,
            "fcf_ratio": 0,
            "ps_value": 0,
            "company_growth": 0,
            "non_gaap": 0,
            "other_ratios": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_all_ratios(data)

    def test_last_year_data(self):
        data = {}
        expected_data = {
            "last_year_inventory": 0,
            "last_year_accounts_payable": 0,
            "last_year_revenue": 0,
            "last_year_net_income": 0,
            "last_year_fcf": 0,
            "last_year_capex": 0,
            "last_year_shares_outstanding": 0,
            "last_year_cost_expense": 0,
            "last_year_cost_revenue": 0,
            "last_year_eps": 0,
            "last_year_research_dev": 0,
            "last_year_fixed_assets": 0,
            "last_year_assets": 0,
            "last_year_owner_earnings": 0,
            "last_year_current_assets": 0,
            "last_year_current_liabilities": 0,
        }
        assert expected_data == CalculateFinancialRatios.last_year_data(data)

    def test_calculate_other_ratios(self):
        data = {
            "last_year_fixed_assets": 5670,
            "last_year_assets": 786578.7568,
            "total_current_assets": 4567.56,
            "total_current_liabilities": 0,
            "last_year_current_assets": 4674560,
            "depreciation_and_amortization": 23476875,
            "operating_income": 567.567,
            "property_plant_equipment_net": 0.65747657,
            "income_tax_expense": 64756,
            "total_debt": 0,
            "total_stockholders_equity": 4365758,
            "cash_and_cash_equivalents": 45460,
        }
        expected_data = {
            "average_fixed_assets": 0,
            "average_assets": 0,
            "net_working_capital": 0,
            "change_in_working_capital": 0,
            "gross_invested_capital": 0,
            "effective_tax_rate": 0,
            "net_tangible_equity": 0,
            "nopat": 0,
            "debt_and_equity": 0,
            "non_cash_working_capital": 0,
            "invested_capital": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_other_ratios(data)

    def test_calculate_rentability_ratios(self):
        data = {
            "total_assets": 3456.456,
            "total_stockholders_equity": 0,
            "operating_income": 34.789,
            "capital_employed": 345.66,
            "net_income": 0,
            "tangible_assets": 3456456,
            "dividends_paid": 345645.6,
            "nopat": 234,
            "invested_capital": 7,
            "gross_invested_capital": 3456456,
        }
        expected_data = {
            "roa": 0,
            "roe": 0,
            "roc": 0,
            "roce": 0,
            "rota": 0,
            "roic": 0,
            "nopat_roic": 0,
            "rogic": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_rentability_ratios(data)

    def test_calculate_liquidity_ratios(self):
        data = {
            "cash_and_cash_equivalents": 0,
            "total_current_assets": 678,
            "net_receivables": 382,
            "cash_and_short_term_investments": 345.34,
            "total_current_liabilities": 34534,
            "net_cash_provided_by_operating_activities": 456.9,
            "total_liabilities": 999,
            "total_stockholders_equity": 0,
        }
        expected_data = {
            "cash_ratio": 0,
            "current_ratio": 0,
            "quick_ratio": 0,
            "operating_cashflow_ratio": 0,
            "debt_to_equity": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_liquidity_ratios(data)

    def test_calculate_margin_ratios(self):
        data = {
            "gross_profit": 9802346,
            "revenue": 9802346,
            "ebitda": 98.02346,
            "net_income": 9802346,
            "free_cash_flow": 98023.46,
            "fcf_equity": 0,
            "unlevered_fcf": 867875,
            "unlevered_fcf_ebit": 234.879,
            "owners_earnings": 0,
        }
        expected_data = {
            "gross_margin": 0,
            "ebitda_margin": 0,
            "net_income_margin": 0,
            "fcf_margin": 0,
            "fcf_equity_to_net_income": 0,
            "unlevered_fcf_to_net_income": 0,
            "unlevered_fcf_ebit_to_net_income": 0,
            "owners_earnings_to_net_income": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_margin_ratios(data)

    def test_calculate_free_cashflow_ratios(self):
        data = {
            "net_cash_provided_by_operating_activities": 9834.569832,
            "debt_repayment": 673245,
            "nopat": 3456456,
            "depreciation_and_amortization": 98.34569832,
            "change_in_working_capital": 3546,
            "operating_income": 0,
            "deferred_income_tax": 567865,
            "net_income": 9834569832,
            "capital_expenditure": 0,
        }
        expected_data = {
            "fcf_equity": 0,
            "unlevered_fcf": 0,
            "unlevered_fcf_ebit": 0,
            "owners_earnings": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_free_cashflow_ratios(data)

    def test_calculate_per_share_value(self):
        data = {
            "revenue": 9458764,
            "weighted_average_shares_outstanding": 56878946764,
            "total_stockholders_equity": 945.8764,
            "net_tangible_equity": 9458.764,
            "free_cash_flow": 0,
            "net_income": 0,
            "cash_and_short_term_investments": 567435,
            "net_cash_provided_by_operating_activities": 3456,
            "capital_expenditure": 456,
            "total_assets": 56.8764,
        }
        expected_data = {
            "sales_ps": 0,
            "book_ps": 0,
            "tangible_ps": 0,
            "fcf_ps": 0,
            "eps": 0,
            "cash_ps": 0,
            "operating_cf_ps": 0,
            "capex_ps": 0,
            "total_assets_ps": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_per_share_value(data)

    def test_calculate_non_gaap(self):
        data = {
            "net_income": 53646,
            "total_other_income_expenses_net": 879789,
            "income_tax_expense": 5465,
            "operating_income": 35645,
            "total_current_assets": 345.345,
            "total_current_liabilities": 45689,
            "last_year_inventory": 9786,
            "inventory": 4657,
            "last_year_accounts_payable": 6575,
            "accounts_payable": 3456,
            "dividends_paid": 53646,
            "common_stock": 53.646,
            "eps": 12,
            "fcf_ps": 53646,
            "current_price": 45,
            "net_cash_provided_by_operating_activities": 5.3646,
            "property_plant_equipment_net": 975786,
            "net_working_capital": 53646,
            "cash_and_cash_equivalents": 530646,
            "weighted_average_shares_outstanding": 5364.6,
            "total_liabilities": 0,
        }
        expected_data = {
            "normalized_income": 0,
            "effective_tax_rate": 0,
            "net_working_capital": 0,
            "average_inventory": 0,
            "average_accounts_payable": 0,
            "dividend_yield": 0,
            "earnings_yield": 0,
            "fcf_yield": 0,
            "income_quality": 0,
            "invested_capital": 0,
            "market_cap": 0,
            "net_current_asset_value": 0,
            "payout_ratio": 0,
            "tangible_assets": 0,
            "retention_ratio": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_non_gaap(data)

    def test_calculate_operation_risk_ratios(self):
        data = {
            "total_assets": 536.46,
            "goodwill_and_intangible_assets": 46763,
            "total_current_liabilities": 5.3646,
            "short_term_debt": 0,
            "interest_expense": 7907,
            "net_cash_provided_by_operating_activities": 98,
            "cash_and_short_term_investments": 5364.6,
            "long_term_debt": 53646,
            "common_stock": 0,
            "total_debt": 53646,
            "debt_and_equity": 13248,
        }
        expected_data = {
            "asset_coverage_ratio": 0,
            "cash_flow_coverage_ratios": 0,
            "cash_coverage": 0,
            "debt_service_coverage": 0,
            "interest_coverage": 0,
            "operating_cashflow_ratio": 0,
            "debt_ratio": 0,
            "long_term_debt_to_capitalization": 0,
            "total_debt_to_capitalization": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_operation_risk_ratios(data)

    def test_calculate_enterprise_value_ratios(self):
        data = {
            "current_price": 345643,
            "weighted_average_shares_outstanding": 547,
            "total_debt": 0,
            "cash_and_short_term_investments": 789,
            "free_cash_flow": 53.646,
            "net_cash_provided_by_operating_activities": 879,
            "revenue": 5364.6,
            "total_assets": 536.46,
            "total_stockholders_equity": 567,
            "ebitda": 0,
        }
        expected_data = {
            "market_cap": 0,
            "enterprise_value": 0,
            "ev_fcf": 0,
            "ev_operating_cf": 0,
            "ev_sales": 0,
            "company_equity_multiplier": 0,
            "ev_multiple": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_enterprise_value_ratios(data)

    def test_calculate_company_growth(self):
        data = {
            "revenue": 234687,
            "last_year_revenue": 124875,
            "cost_of_revenue": 2457.56,
            "last_year_cost_revenue": 2356,
            "cost_and_expenses": 23487,
            "last_year_cost_expense": 7854,
            "net_income": 234654,
            "last_year_net_income": 0,
            "weighted_average_shares_outstanding": 53.646,
            "last_year_shares_outstanding": 53.646,
            "eps": 536.46,
            "last_year_eps": 6879,
            "free_cash_flow": 5364.6,
            "last_year_fcf": 0,
            "owners_earnings": 53.646,
            "last_year_owner_earnings": 536.46,
            "capital_expenditure": 0,
            "last_year_capex": 53646,
            "rd_expenses": 0,
            "last_year_research_dev": 536.46,
        }
        expected_data = {
            "revenue_growth": 0,
            "cost_revenue_growth": 0,
            "operating_expenses_growth": 0,
            "net_income_growth": 0,
            "shares_buyback": 0,
            "eps_growth": 0,
            "fcf_growth": 0,
            "owners_earnings_growth": 0,
            "capex_growth": 0,
            "rd_expenses_growth": 0,
        }
        assert expected_data == CalculateFinancialRatios.calculate_company_growth(data)

    def test_calculate_efficiency_ratios(self):
        expected_data = {
            "accounts_payable_turnover": 0.333,
            "asset_turnover": 0.857,
            "cash_conversion_cycle": 334.70640000000003,
            "days_inventory_outstanding": 0.0014,
            "days_payables_outstanding": 273.75,
            "days_sales_outstanding": 608.455,
            "fixed_asset_turnover": 0.75,
            "free_cashflow_to_operating_cashflow": 0.909,
            "inventory_turnover": 2.0,
            "operating_cycle": 608.46,
        }

        data = {
            "average_inventory": 100,
            "cost_of_revenue": 200,
            "accounts_payable": 300,
            "cost_of_goods_sold": 400,
            "accounts_receivable": 500,
            "revenue": 600,
            "average_assets": 700,
            "average_fixed_assets": 800,
            "average_accounts_payable": 900,
            "free_cash_flow": 1000,
            "net_cash_provided_by_operating_activities": 1100,
        }
        assert expected_data == CalculateFinancialRatios.calculate_efficiency_ratios(data)

    def test_calculate_price_to_ratios(self):
        expected_data = {
            "price_book": 1.0,
            "price_cf": 5.0,
            "price_earnings": 4.72,
            "price_earnings_growth": 18.88,
            "price_sales": 2.94,
            "price_total_assets": 3.33,
            "price_fcf": 1.45,
            "price_operating_cf": 0,
            "price_tangible_assets": 0.83,
        }
        data = {
            "book_ps": 10,
            "cash_ps": 2,
            "current_price": 10,
            "eps": 2.12,
            "net_income_growth": 0.25,
            "sales_ps": 3.4,
            "total_assets_ps": 3,
            "fcf_ps": 6.92,
            "operating_cf_ps": 0,
            "tangible_ps": 12.12,
        }
        assert expected_data == CalculateFinancialRatios.calculate_price_to_ratios(data)
