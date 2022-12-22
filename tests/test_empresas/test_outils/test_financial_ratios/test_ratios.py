from django.test import TestCase
from django.utils import timezone

from bfet import DjangoTestingModel

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.periods.models import Period
from src.periods.constants import PERIOD_FOR_YEAR

from tests.data.empresas import (
    balance_sheets_final_statment,
    income_final_statment,
    cashflow_final_statment,
)

class TestCalculateFinancialRatios(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.current_year = timezone.now().year
        cls.previous_year = cls.current_year - 1
        current_period = DjangoTestingModel.create(Period, period=PERIOD_FOR_YEAR, year=cls.current_year)
        previous_period = DjangoTestingModel.create(Period, period=PERIOD_FOR_YEAR, year=cls.previous_year)
        cls.company = DjangoTestingModel.create(Company)
        cls.current_income = DjangoTestingModel.create(
            IncomeStatement,
            period=current_period,
            company=cls.company,
            **income_final_statment.CURRENT_YEAR,
        )
        cls.current_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=current_period,
            company=cls.company,
            **balance_sheets_final_statment.CURRENT_YEAR,
        )
        cls.current_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=current_period,
            company=cls.company,
            **cashflow_final_statment.CURRENT_YEAR,
        )
        cls.previous_income = DjangoTestingModel.create(
            IncomeStatement,
            period=previous_period,
            company=cls.company,
            **income_final_statment.PAST_YEAR,
        )
        cls.previous_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=previous_period,
            company=cls.company,
            **balance_sheets_final_statment.PAST_YEAR,
        )
        cls.previous_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=previous_period,
            company=cls.company,
            **cashflow_final_statment.PAST_YEAR,
        )

    def test_split_statements_by_year(self):
        current, previous = CalculateFinancialRatios(self.company).split_statements_by_year(2022, 5)
        assert [
                   self.current_income,
                   self.current_balance,
                   self.current_cashflow,
               ] == current
        assert [
                   self.previous_income,
                   self.previous_balance,
                   self.previous_cashflow,
               ] == previous

    def test_prepare_base_data(self):
        inc_statements = self.company.inc_statements.filter(period__period=PERIOD_FOR_YEAR)
        balance_sheets = self.company.balance_sheets.filter(period__period=PERIOD_FOR_YEAR)
        cf_statements = self.company.cf_statements.filter(period__period=PERIOD_FOR_YEAR)
        base_data = CalculateFinancialRatios.prepare_base_data(
            inc_statements.filter(period__year=self.current_year).values(),
            balance_sheets.filter(period__year=self.current_year).values(),
            cf_statements.filter(period__year=self.current_year).values(),
            inc_statements.filter(period__year=self.previous_year).values(),
            balance_sheets.filter(period__year=self.previous_year).values(),
            cf_statements.filter(period__year=self.previous_year).values(),
            {"current_price": 34.65}
        )
        assert isinstance(base_data, dict)


    def test_calculate_all_ratios(self):
        expected_result = {
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

        assert expected_result == CalculateFinancialRatios.calculate_all_ratios(
            IncomeStatement.objects.filter(period=self.current_year).values(),
            BalanceSheet.objects.filter(period=self.current_year).values(),
            CashflowStatement.objects.filter(period=self.current_year).values(),
            IncomeStatement.objects.filter(period=self.previous_year).values(),
            BalanceSheet.objects.filter(period=self.previous_year).values(),
            CashflowStatement.objects.filter(period=self.previous_year).values(),
            {"current_price": 45.32},
        )

    def test_filter_previous_year_data(self):
        data = {
            "inventory": 3546,
            "accounts_payable": 678,
            "revenue": 345,
            "net_income": 578.6,
            "free_cash_flow": 79,
            "weighted_average_shares_outstanding": 378,
            "cost_and_expenses": 285.7,
            "cost_of_revenue": 6855,
            "rd_expenses": 8675.6,
            "property_plant_equipment_net": 576.845,
            "total_assets": 54564,
            "depreciation_and_amortization": 234.67,
            "change_in_working_capital": 756.34,
            "capital_expenditure": 3546,
            "total_current_assets": 35.46,
            "total_current_liabilities": 567,
        }
        expected_result = {
            "last_year_inventory": 3546,
            "last_year_accounts_payable": 678,
            "last_year_revenue": 345,
            "last_year_net_income": 578.6,
            "last_year_fcf": 79,
            "last_year_capex": 3546,
            "last_year_shares_outstanding": 378,
            "last_year_cost_expense": 285.7,
            "last_year_cost_revenue": 6855,
            "last_year_eps": 1.5307,
            "last_year_research_dev": 8675.6,
            "last_year_fixed_assets": 576.845,
            "last_year_assets": 54564,
            "last_year_owner_earnings": 5115.610000000001,
            "last_year_current_assets": 35.46,
            "last_year_current_liabilities": 567,
        }
        assert expected_result == CalculateFinancialRatios.filter_previous_year_data(data)

    def test_calculate_other_ratios(self):
        data = {
            "last_year_fixed_assets": 4326.36,
            "last_year_assets": 5464,
            "total_assets": 67578,
            "total_current_liabilities": 6580,
            "last_year_current_assets": 0,
            "last_year_current_liabilities": 97234,
            "property_plant_equipment_net": 293847,
            "depreciation_and_amortization": 982.347,
            "income_tax_expense": 982346,
            "operating_income": 24556,
            "total_current_assets": 35.468,
            "total_liabilities": 234875,
            "total_debt": 456723,
            "total_stockholders_equity": 293.487,
            "cash_and_cash_equivalents": 1289,
            "common_stocks": 345758,
            "current_price": 45,
            "retained_earnings": 65765,
            "preferred_stocks": 5678,
            "long_term_debt": 768,
        }
        expected_result = {
            "average_fixed_assets": 149086.68,
            "average_assets": 36521.0,
            "net_working_capital": -6544.532,
            "change_in_working_capital": -103778.532,
            "gross_invested_capital": 288284.815,
            "effective_tax_rate": 40.0,
            "net_tangible_equity": 59007.46799999999,
            "nopat": -957684.0,
            "debt_and_equity": 457016.487,
            "non_cash_working_capital": -7833.532,
            "invested_capital": 15881153,
            "common_equity": 15624875,
            "preferred_equity": 255510,
        }
        assert expected_result == CalculateFinancialRatios.calculate_other_ratios(data)

    def test_calculate_rentability_ratios(self):
        data = {
            "total_assets": 3456.456,
            "total_stockholders_equity": 0,
            "operating_income": 34.789,
            "capital_employed": 345.66,
            "net_income": 345,
            "tangible_assets": 5656,
            "dividends_paid": 3445.6,
            "nopat": 234,
            "invested_capital": 7,
            "gross_invested_capital": 987,
        }
        expected_result = {
            "roa": 10.0,
            "roe": 0,
            "roc": 1.0,
            "roce": 10.0,
            "rota": 6.0,
            "roic": -44294.0,
            "nopat_roic": 3343.0,
            "rogic": 24.0,
        }
        assert expected_result == CalculateFinancialRatios.calculate_rentability_ratios(data)

    def test_calculate_liquidity_ratios(self):
        data = {
            "cash_and_cash_equivalents": 4756.56,
            "total_current_assets": 678,
            "net_receivables": 382,
            "cash_and_short_term_investments": 345.34,
            "total_current_liabilities": 34534,
            "net_cash_provided_by_operating_activities": 456.9,
            "total_liabilities": 999,
            "total_stockholders_equity": 5670,
        }
        expected_result = {
            "cash_ratio": 0.14,
            "current_ratio": 0.02,
            "quick_ratio": 0.02,
            "operating_cashflow_ratio": 0.01,
            "debt_to_equity": 0.18,
        }
        assert expected_result == CalculateFinancialRatios.calculate_liquidity_ratios(data)

    def test_calculate_margin_ratios(self):
        data = {
            "gross_profit": 946,
            "revenue": 346,
            "ebitda": 98.02346,
            "net_income": 98346,
            "free_cash_flow": 8023.46,
            "fcf_equity": 6547,
            "unlevered_fcf": 7875,
            "unlevered_fcf_ebit": 234.879,
            "owners_earnings": 57867,
        }
        expected_result = {
            "gross_margin": 273.0,
            "ebitda_margin": 28.0,
            "net_income_margin": 28424.0,
            "fcf_margin": 2319.0,
            "fcf_equity_to_net_income": 7.0,
            "unlevered_fcf_to_net_income": 8.0,
            "unlevered_fcf_ebit_to_net_income": 0.0,
            "owners_earnings_to_net_income": 59.0,
        }
        assert expected_result == CalculateFinancialRatios.calculate_margin_ratios(data)

    def test_calculate_free_cashflow_ratios(self):
        data = {
            "net_cash_provided_by_operating_activities": 9834.569832,
            "debt_repayment": 6245,
            "nopat": 3456,
            "depreciation_and_amortization": 98.34569832,
            "change_in_working_capital": 3546,
            "operating_income": 5487,
            "deferred_income_tax": 5865,
            "net_income": 989832,
            "capital_expenditure": 7869,
        }
        expected_result = {
            "fcf_equity": 23948.569832,
            "unlevered_fcf": 14969.34569832,
            "unlevered_fcf_ebit": 22865.34569832,
            "owners_earnings": 1001345.34569832,
        }
        assert expected_result == CalculateFinancialRatios.calculate_free_cashflow_ratios(data)

    def test_calculate_per_share_value(self):
        data = {
            "revenue": 94564,
            "weighted_average_shares_outstanding": 568764,
            "total_stockholders_equity": 945.8764,
            "net_tangible_equity": 9458.764,
            "free_cash_flow": 8679,
            "net_income": 678,
            "cash_and_short_term_investments": 567435,
            "net_cash_provided_by_operating_activities": 3456,
            "capital_expenditure": 456,
            "total_assets": 56.8764,
        }
        expected_result = {
            "sales_ps": 0.1663,
            "book_ps": 0.0017,
            "tangible_ps": 0.0166,
            "fcf_ps": 0.0153,
            "eps": 0.0012,
            "cash_ps": 0.9977,
            "operating_cf_ps": 0.0061,
            "capex_ps": 0.0008,
            "total_assets_ps": 0.0001,
        }
        assert expected_result == CalculateFinancialRatios.calculate_per_share_value(data)

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
        expected_result = {
            "normalized_income": -826143,
            "effective_tax_rate": 0.15,
            "net_working_capital": -45343.655,
            "average_inventory": 7221.5,
            "average_accounts_payable": 5015.5,
            "dividend_yield": 2222.0,
            "earnings_yield": 27.0,
            "fcf_yield": 119213.0,
            "income_quality": 0.0,
            "invested_capital": 1560078,
            "market_cap": 0.01,
            "net_current_asset_value": 0.06,
            "payout_ratio": 100.0,
            "tangible_assets": 976131.345,
            "retention_ratio": 0.0,
        }
        assert expected_result == CalculateFinancialRatios.calculate_non_gaap(data)

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
        expected_result = {
            "asset_coverage_ratio": -5.85,
            "cash_flow_coverage_ratios": 0.0,
            "cash_coverage": 0.68,
            "debt_service_coverage": 0.0,
            "interest_coverage": 0.0,
            "operating_cashflow_ratio": 18.27,
            "debt_ratio": 100.0,
            "long_term_debt_to_capitalization": 1.0,
            "total_debt_to_capitalization": 4.05,
        }
        assert expected_result == CalculateFinancialRatios.calculate_operation_risk_ratios(data)

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
        expected_result = {
            "market_cap": 631.89,
            "enterprise_value": -157.11,
            "ev_fcf": -2.93,
            "ev_operating_cf": -0.18,
            "ev_sales": -0.03,
            "company_equity_multiplier": 0.95,
            "ev_multiple": 0,
        }
        assert expected_result == CalculateFinancialRatios.calculate_enterprise_value_ratios(data)

    def test_calculate_company_growth(self):
        data = {
            "revenue": 234687,
            "last_year_revenue": 124875,
            "cost_of_revenue": 2457.56,
            "last_year_cost_revenue": 2356,
            "cost_and_expenses": 23487,
            "last_year_cost_expense": 7854,
            "net_income": 234654,
            "last_year_net_income": 56756,
            "weighted_average_shares_outstanding": 53.646,
            "last_year_shares_outstanding": 53.646,
            "eps": 536.46,
            "last_year_eps": 6879,
            "free_cash_flow": 5364.6,
            "last_year_fcf": 56857,
            "owners_earnings": 53.646,
            "last_year_owner_earnings": 536.46,
            "capital_expenditure": 67867,
            "last_year_capex": 53646,
            "rd_expenses": 67867,
            "last_year_research_dev": 536.46,
        }
        expected_result = {
            "revenue_growth": 88.0,
            "cost_revenue_growth": 4.0,
            "operating_expenses_growth": 199.0,
            "net_income_growth": 313.0,
            "shares_buyback": 0.0,
            "eps_growth": -92.0,
            "fcf_growth": -91.0,
            "owners_earnings_growth": -90.0,
            "capex_growth": 27.0,
            "rd_expenses_growth": 12551.0,
        }
        assert expected_result == CalculateFinancialRatios.calculate_company_growth(data)

    def test_calculate_efficiency_ratios(self):
        expected_result = {
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
        assert expected_result == CalculateFinancialRatios.calculate_efficiency_ratios(data)

    def test_calculate_price_to_ratios(self):
        expected_result = {
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
        assert expected_result == CalculateFinancialRatios.calculate_price_to_ratios(data)
