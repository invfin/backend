from unittest.mock import patch

from freezegun import freeze_time
from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.outils.data_management.show.company_data import CompanyData
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.data_management.update.update import UpdateCompany
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from tests.data.empresas import (
    balance_sheets_final_statment,
    cashflow_final_statment,
    income_final_statment,
)
from src.empresas.outils.data_management.interfaces import (
    StatementsInterface,
    AveragesInterface,
)

EMPRESA_DATA_MNGMT = "src.empresas.outils.data_management"

INFO_SOURCES = f"{EMPRESA_DATA_MNGMT}.information_sources"
COMPANY_DATA = f"{EMPRESA_DATA_MNGMT}.show.company_data.CompanyData"


class TestCompanyData(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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
        cls.company = DjangoTestingModel.create(Company, ticker="AAPL")
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
        cls.company_data = CompanyData(cls.company)

    def test_get_statements(self):
        self.assertTrue(isinstance(self.company_data.get_statements(), StatementsInterface))

    def test_get_averages(self):
        self.assertTrue(isinstance(self.company_data.get_averages(), AveragesInterface))

    @patch(f"{COMPANY_DATA}.mock_get_yahooquery_price")
    @patch(f"{COMPANY_DATA}.get_yfinance_price")
    def test_get_most_recent_price_yf_none(
        self,
        mock_get_yfinance_price,
        mock_get_yahooquery_price,
    ):
        mock_get_yfinance_price.return_value = None
        mock_get_yahooquery_price.return_value = 5
        self.assertEqual(self.company_data.get_most_recent_price(), 5)
        mock_get_yfinance_price.assert_called_once()
        mock_get_yahooquery_price.assert_called_once()

    @patch(f"{COMPANY_DATA}.mock_get_yahooquery_price")
    @patch(f"{COMPANY_DATA}.get_yfinance_price")
    def test_get_most_recent_price_yq_none(
        self,
        mock_get_yfinance_price,
        mock_get_yahooquery_price,
    ):
        mock_get_yfinance_price.return_value = 5
        mock_get_yahooquery_price.return_value = None
        self.assertEqual(self.company_data.get_most_recent_price(), 5)
        mock_get_yfinance_price.assert_called_once()
        mock_get_yahooquery_price.assert_called_once()

    @patch(f"{COMPANY_DATA}.mock_get_yahooquery_price")
    @patch(f"{COMPANY_DATA}.get_yfinance_price")
    def test_get_most_recent_price(
        self,
        mock_get_yfinance_price,
        mock_get_yahooquery_price,
    ):
        mock_get_yfinance_price.return_value = mock_get_yahooquery_price.return_value = None
        self.assertEqual(self.company_data.get_most_recent_price(), 0)
        mock_get_yfinance_price.assert_called_once()
        mock_get_yahooquery_price.assert_called_once()

    @patch(f"{INFO_SOURCES}.YFinanceInfo.request_info_yfinance")
    def test_get_yfinance_price(self, mock_request_info_yfinance):
        mock_request_info_yfinance.return_value = {"currentPrice": 5}
        self.assertEqual(self.company_data.get_yfinance_price(), 5)
        mock_request_info_yfinance.assert_called_once()

    @patch(f"{INFO_SOURCES}.YahooQueryInfo.yahooquery.request_price_info_yahooquery")
    def test_get_yahooquery_price(self, mock_request_price_info_yahooquery):
        mock_request_price_info_yahooquery.return_value = {"regularMarketPrice": 5}
        self.assertEqual(self.company_data.get_yfinance_price(), 5)
        mock_request_price_info_yahooquery.assert_called_once()

    @freeze_time("12-12-2022")
    @patch(f"{INFO_SOURCES}.FinnhubInfo.company_news")
    def test_get_company_news(self, mock_company_news):
        mock_company_news.return_value = ["news"]
        self.assertEqual(self.company_data.get_company_news(), ["news"])
        mock_company_news.assert_called_once_with("AAPL", "2022-12-10", "2022-12-12")
