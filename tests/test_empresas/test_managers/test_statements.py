from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.data_management.update.update import UpdateCompany
from src.periods.constants import PERIOD_1_QUARTER, PERIOD_FOR_YEAR
from src.periods.models import Period
from tests.data.empresas import (
    balance_sheets_final_statment,
    cashflow_final_statment,
    income_final_statment,
)


class TestBaseStatementQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_period = DjangoTestingModel.create(
            Period,
            year=2021,
            period=PERIOD_FOR_YEAR,
        )
        cls.previous_period = DjangoTestingModel.create(
            Period,
            year=2020,
            period=PERIOD_FOR_YEAR,
        )
        cls.current_quarter_period = DjangoTestingModel.create(
            Period,
            year=2021,
            period=PERIOD_1_QUARTER,
        )
        cls.previous_quarter_period = DjangoTestingModel.create(
            Period,
            year=2020,
            period=PERIOD_1_QUARTER,
        )
        cls.company = DjangoTestingModel.create(Company)
        cls.current_income = DjangoTestingModel.create(
            IncomeStatement,
            is_ttm=False,
            from_average=False,
            period=cls.current_period,
            company=cls.company,
        )
        cls.previous_income = DjangoTestingModel.create(
            IncomeStatement,
            is_ttm=False,
            from_average=False,
            period=cls.previous_period,
            company=cls.company,
        )
        cls.current_quarter_income = DjangoTestingModel.create(
            IncomeStatement,
            is_ttm=False,
            from_average=False,
            period=cls.current_quarter_period,
            company=cls.company,
        )
        cls.previous_quarter_income = DjangoTestingModel.create(
            IncomeStatement,
            is_ttm=False,
            from_average=False,
            period=cls.previous_quarter_period,
            company=cls.company,
        )

    def test_quarterly(self):
        income_statements = list(self.company.inc_statements.quarterly())
        assert self.current_quarter_income in income_statements
        assert self.previous_quarter_income in income_statements
        assert self.current_income not in income_statements
        assert self.previous_income not in income_statements

    def test_yearly(self):
        income_statements = list(self.company.inc_statements.yearly())
        assert self.current_income in income_statements
        assert self.previous_income in income_statements
        assert self.current_quarter_income not in income_statements
        assert self.previous_quarter_income not in income_statements


class TestStatementQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_period = DjangoTestingModel.create(
            Period, year=2021, period=PERIOD_FOR_YEAR
        )
        cls.previous_period = DjangoTestingModel.create(
            Period, year=2020, period=PERIOD_FOR_YEAR
        )
        cls.company = DjangoTestingModel.create(Company)
        cls.current_income = DjangoTestingModel.create(
            IncomeStatement,
            period=cls.current_period,
            company=cls.company,
            **income_final_statment.CURRENT_YEAR,
        )
        cls.current_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=cls.current_period,
            company=cls.company,
            **balance_sheets_final_statment.CURRENT_YEAR,
        )
        cls.current_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=cls.current_period,
            company=cls.company,
            **cashflow_final_statment.CURRENT_YEAR,
        )
        cls.previous_income = DjangoTestingModel.create(
            IncomeStatement,
            period=cls.previous_period,
            company=cls.company,
            **income_final_statment.PAST_YEAR,
        )
        cls.previous_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=cls.previous_period,
            company=cls.company,
            **balance_sheets_final_statment.PAST_YEAR,
        )
        cls.previous_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=cls.previous_period,
            company=cls.company,
            **cashflow_final_statment.PAST_YEAR,
        )
        all_ratios = CalculateFinancialRatios.calculate_all_ratios(
            cls.company.inc_statements.filter(period=cls.current_period).values(),
            cls.company.balance_sheets.filter(period=cls.current_period).values(),
            cls.company.cf_statements.filter(period=cls.current_period).values(),
            cls.company.inc_statements.filter(period=cls.previous_period).values(),
            cls.company.balance_sheets.filter(period=cls.previous_period).values(),
            cls.company.cf_statements.filter(period=cls.previous_period).values(),
            {"current_price": 34.65},
        )
        UpdateCompany(cls.company).create_or_update_all_ratios(all_ratios, cls.current_period)

    def test_average_margins(self):
        assert self.company.margins.all().average_margins() == {
            "average_gross_margin": 42.0,
            "average_ebitda_margin": 34.0,
            "average_net_income_margin": -26.0,
            "average_fcf_margin": 0.0,
            "average_fcf_equity_to_net_income": 9.0,
            "average_unlevered_fcf_to_net_income": 257.0,
            "average_unlevered_fcf_ebit_to_net_income": 262.0,
            "average_owners_earnings_to_net_income": 357.0,
        }

    def test_average_efficiency_ratios(self):
        assert self.company.efficiency_ratios.all().average_efficiency_ratios() == {
            "average_asset_turnover": 1.084,
            "average_inventory_turnover": -153.832,
            "average_fixed_asset_turnover": 0.0,
            "average_accounts_payable_turnover": 2.983,
            "average_cash_conversion_cycle": -299.66499999999996,
            "average_days_inventory_outstanding": 0.0,
            "average_days_payables_outstanding": 0.0,
            "average_days_sales_outstanding": -299.66499999999996,
            "average_free_cashflow_to_operating_cashflow": 0.0,
            "average_operating_cycle": -299.66,
        }

    def test_average_growth_rates(self):
        assert self.company.growth_rates.all().average_growth_rates() == {
            "average_revenue_growth": 33.0,
            "average_cost_revenue_growth": 26.0,
            "average_operating_expenses_growth": 23.0,
            "average_net_income_growth": 795.0,
            "average_shares_buyback": -4.0,
            "average_eps_growth": 830.0,
            "average_fcf_growth": 0.0,
            "average_owners_earnings_growth": 6920.0,
            "average_capex_growth": 0.0,
            "average_rd_expenses_growth": 0.0,
        }

    def test_average_per_share_values(self):
        assert self.company.per_share_values.all().average_per_share_values() == {
            "average_sales_ps": 21.691,
            "average_book_ps": 3.7409,
            "average_tangible_ps": -9.0766,
            "average_fcf_ps": 0.0,
            "average_eps": -5.5353,
            "average_cash_ps": 3.7142,
            "average_operating_cf_ps": 0.0,
            "average_capex_ps": 0.0,
            "average_total_assets_ps": 20.8126,
        }

    def test_average_price_to_ratios(self):
        assert self.company.price_to_ratios.all().average_price_to_ratios() == {
            "average_price_book": 9.26,
            "average_price_cf": 9.33,
            "average_price_earnings": -6.26,
            "average_price_earnings_growth": -0.01,
            "average_price_sales": 1.6,
            "average_price_total_assets": 1.66,
            "average_price_fcf": 0.0,
            "average_price_operating_cf": 0.0,
            "average_price_tangible_assets": -3.82,
        }

    def test_average_liquidity_ratios(self):
        assert self.company.liquidity_ratios.all().average_liquidity_ratios() == {
            "average_cash_ratio": 0.28,
            "average_current_ratio": 1.07,
            "average_quick_ratio": 0.91,
            "average_operating_cashflow_ratio": 0.0,
            "average_debt_to_equity": 4.56,
        }

    def test_average_rentability_ratios(self):
        assert self.company.rentability_ratios.all().average_rentability_ratios() == {
            "average_roa": -27.0,
            "average_roe": -148.0,
            "average_roc": 0.0,
            "average_roce": 0.0,
            "average_rota": -69.0,
            "average_roic": -178.0,
            "average_nopat_roic": 0.0,
            "average_rogic": 0.0,
        }

    def test_average_operation_risks_ratios(self):
        assert self.company.operation_risks_ratios.all().average_operation_risks_ratios() == {
            "average_asset_coverage_ratio": 79.36,
            "average_cash_flow_coverage_ratios": 0.0,
            "average_cash_coverage": 23.68,
            "average_debt_service_coverage": 0.0,
            "average_interest_coverage": 0.0,
            "average_operating_cashflow_ratio": 0.0,
            "average_debt_ratio": 0.36,
            "average_long_term_debt_to_capitalization": 1.0,
            "average_total_debt_to_capitalization": 0.66,
        }

    def test_average_ev_ratios(self):
        assert self.company.ev_ratios.all().average_ev_ratios() == {
            "average_ev_fcf": 0.0,
            "average_ev_operating_cf": 0.0,
            "average_ev_sales": 0.17,
            "average_company_equity_multiplier": 5.56,
            "average_ev_multiple": 0.5,
        }
