from unittest.mock import patch

from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import BalanceSheetYahooQuery, Company
from src.empresas.information_sources.yahoo_query import NormalizeYahooQuery, YahooQueryInfo
from src.periods.constants import PERIOD_1_QUARTER
from src.periods.models import Period
from tests.data.empresas.yahooquery import balance_dataframe


class TestYahooQueryInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DjangoTestingModel.create(Company, ticker="AAPL")
        cls.parser = YahooQueryInfo(cls.company)

    def test_create_statements_from_df_balance(self):
        # TODO: improve this test
        assert (
            0
            == BalanceSheetYahooQuery.objects.filter(
                company=self.company,
                period__period=PERIOD_1_QUARTER,
            ).count()
        )
        self.parser.create_statements_from_df(
            balance_dataframe().fillna(0),
            Period.objects.first_quarter_period,
            NormalizeYahooQuery.normalize_balance_sheets_yahooquery,
            BalanceSheetYahooQuery,
        )
        assert (
            4
            == BalanceSheetYahooQuery.objects.filter(
                company=self.company,
                period__period=PERIOD_1_QUARTER,
            ).count()
        )

    @patch("src.empresas.parse.yahoo_query.YahooQueryInfo.create_financials")
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_income_statements_yahooquery"
    )
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_balance_sheets_yahooquery"
    )
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_cashflow_statements_yahooquery"
    )
    def test_create_quarterly_financials_yahooquery(
        self,
        mock_req_cashflow_statement,
        mock_req_balance_sheet,
        mock_req_income_statement,
        mock_create_financials,
    ):
        mock_req_income_statement.return_value = "mock_req_income_statement"
        mock_req_balance_sheet.return_value = "mock_req_balance_sheet"
        mock_req_cashflow_statement.return_value = "mock_req_cashflow_statement"
        self.parser.create_quarterly_financials_yahooquery()
        mock_req_income_statement.assert_called_once_with("q")
        mock_req_balance_sheet.assert_called_once_with("q")
        mock_req_cashflow_statement.assert_called_once_with("q")
        mock_create_financials.assert_called_once_with(
            "mock_req_income_statement",
            "mock_req_balance_sheet",
            "mock_req_cashflow_statement",
            Period.objects.first_quarter_period,
        )

    @patch("src.empresas.parse.yahoo_query.YahooQueryInfo.create_financials")
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_income_statements_yahooquery"
    )
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_balance_sheets_yahooquery"
    )
    @patch(
        "src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_cashflow_statements_yahooquery"
    )
    def test_create_yearly_financials_yahooquery(
        self,
        mock_req_cashflow_statement,
        mock_req_balance_sheet,
        mock_req_income_statement,
        mock_create_financials,
    ):
        mock_req_income_statement.return_value = "mock_req_income_statement"
        mock_req_balance_sheet.return_value = "mock_req_balance_sheet"
        mock_req_cashflow_statement.return_value = "mock_req_cashflow_statement"
        self.parser.create_yearly_financials_yahooquery()
        mock_req_income_statement.assert_called_once_with()
        mock_req_balance_sheet.assert_called_once_with()
        mock_req_cashflow_statement.assert_called_once_with()
        mock_create_financials.assert_called_once_with(
            "mock_req_income_statement",
            "mock_req_balance_sheet",
            "mock_req_cashflow_statement",
            Period.objects.for_year_period,
        )
