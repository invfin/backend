from unittest.mock import patch

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

    def test_generate_limit(self):
        assert 2 == len(CompanyData.generate_limit(self.company.inc_statements.all(), 0))
        assert 1 == len(CompanyData.generate_limit(self.company.inc_statements.all(), 1))

    @patch("src.empresas.extensions.new_company_extension.CompanyData.income_json")
    @patch("src.general.utils.ChartSerializer.generate_json")
    def test_build_table_and_chart(self, mock_generate_json, mock_income_json):
        mock_generate_json.return_value = "value"
        mock_income_json.return_value = "value"
        statement = self.company.inc_statements.all()
        result = CompanyData.build_table_and_chart(
            statement,
            CompanyData.income_to_json,
        )
        mock_income_json.assert_called_once_with(statement)
        mock_generate_json.assert_called_once_with("value", None, "line")
        self.assertDictEqual(result, {"table": "value", "chart": "value"})

    def test_income_json(self):
        company_data = CompanyData(self.company).income_json(self.company.inc_statements.all())
        assert company_data == {
            "currency": "$",
            "labels": ["2021", "2020"],
            "fields": [
                {
                    "title": "Ingresos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [365817000000.0, 274515000000.0],
                },
                {
                    "title": "Costos de venta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [212981000000.0, 169559000000.0],
                },
                {
                    "title": "Utilidad bruta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [152836000000.0, 104956000000.0],
                },
                {"title": "I&D", "url": "#!", "percent": "false", "short": "false", "values": [0.0, 0.0]},
                {
                    "title": "Gastos administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Gastos marketing",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [21973000000.0, 19916000000.0],
                },
                {
                    "title": "Gastos marketing, generales y administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-258000000.0, -803000000.0],
                },
                {
                    "title": "Gastos otros",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [21914000000.0, 18752000000.0],
                },
                {
                    "title": "Gastos operativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [108949000000.0, 66288000000.0],
                },
                {
                    "title": "Gastos y costos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [256868000000.0, 208227000000.0],
                },
                {
                    "title": "Intereses",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [2645000000.0, 2873000000.0],
                },
                {
                    "title": "Depreciación & Amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [11284000000.0, 11056000000.0],
                },
                {
                    "title": "EBITDA",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [123136000000.0, 81020000000.0],
                },
                {
                    "title": "Ingresos de explotación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Otros Gastos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [43887000000.0, 38668000000.0],
                },
                {
                    "title": "EBT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [109207000000.0, 67091000000.0],
                },
                {
                    "title": "Impuestos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [14527000000.0, 9680000000.0],
                },
                {
                    "title": "Ingresos netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [94680000000.0, 57411000000.0],
                },
                {
                    "title": "Acciones en circulación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [16864919000.0, 17528214000.0],
                },
                {
                    "title": "Acciones diluidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [16701272000.0, 17352119000.0],
                },
            ],
        }
