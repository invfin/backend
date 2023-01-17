from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.extensions.new_company_extension import CompanyData
from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.update import UpdateCompany
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from tests.data.empresas import balance_sheets_final_statment, cashflow_final_statment, income_final_statment


class TestCompanyData(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.current_period = DjangoTestingModel.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.previous_period = DjangoTestingModel.create(Period, year=2020, period=PERIOD_FOR_YEAR)
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

    def test_get_statements(self):
        statements = CompanyData(self.company).get_statements()
        assert "inc_statements" in statements
        assert "balance_sheets" in statements
        assert "cf_statements" in statements
        assert "rentability_ratios" in statements
        assert "liquidity_ratios" in statements
        assert "margins" in statements
        assert "fcf_ratios" in statements
        assert "per_share_values" in statements
        assert "non_gaap_figures" in statements
        assert "operation_risks_ratios" in statements
        assert "ev_ratios" in statements
        assert "growth_rates" in statements
        assert "efficiency_ratios" in statements
        assert "price_to_ratios" in statements

    def test_get_averages(self):
        company_data = CompanyData(self.company)
        statements = company_data.get_averages(company_data.get_statements())
        # assert "inc_statements_averages" in statements
        # assert "balance_sheets_averages" in statements
        # assert "cf_statements_averages" in statements
        assert "rentability_ratios_averages" in statements
        assert "liquidity_ratios_averages" in statements
        assert "margins_averages" in statements
        # assert "fcf_ratios_averages" in statements
        assert "per_share_values_averages" in statements
        # assert "non_gaap_figures_averages" in statements
        assert "operation_risks_ratios_averages" in statements
        assert "ev_ratios_averages" in statements
        assert "growth_rates_averages" in statements
        assert "efficiency_ratios_averages" in statements
        assert "price_to_ratios_averages" in statements
        assert "inc_statements" in statements
        assert "balance_sheets" in statements
        assert "cf_statements" in statements
        assert "rentability_ratios" in statements
        assert "liquidity_ratios" in statements
        assert "margins" in statements
        assert "fcf_ratios" in statements
        assert "per_share_values" in statements
        assert "non_gaap_figures" in statements
        assert "operation_risks_ratios" in statements
        assert "ev_ratios" in statements
        assert "growth_rates" in statements
        assert "efficiency_ratios" in statements
        assert "price_to_ratios" in statements
