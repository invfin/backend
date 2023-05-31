from unittest.mock import patch

from django.test import TestCase

from src.empresas.information_sources.finprep.parse_data import ParseFinprep


PARSE_FINPREP = "src.empresas.parse.finprep.parse_data.ParseFinprep"


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()
        cls.ticker = "AAPL"
        cls.dict_params = {"limit": 11}

    @patch(f"{PARSE_FINPREP}.request")
    def test_request_income_statements_finprep(self, mock_request):
        self.parser.request_income_statements_finprep(self.ticker, self.dict_params)
        mock_request.assert_called_once_with(
            path="income-statement",
            str_params=self.ticker,
            dict_params=self.dict_params,
        )

    @patch(f"{PARSE_FINPREP}.request")
    def test_request_balance_sheets_finprep(self, mock_request):
        self.parser.request_balance_sheets_finprep(self.ticker, self.dict_params)
        mock_request.assert_called_once_with(
            path="balance-sheet-statement",
            str_params=self.ticker,
            dict_params=self.dict_params,
        )

    @patch(f"{PARSE_FINPREP}.request")
    def test_request_cashflow_statements_finprep(self, mock_request):
        self.parser.request_cashflow_statements_finprep(self.ticker, self.dict_params)
        mock_request.assert_called_once_with(
            path="cash-flow-statement",
            str_params=self.ticker,
            dict_params=self.dict_params,
        )

    @patch(f"{PARSE_FINPREP}.request_income_statements_finprep")
    @patch(f"{PARSE_FINPREP}.request_balance_sheets_finprep")
    @patch(f"{PARSE_FINPREP}.request_cashflow_statements_finprep")
    def test_request_financials_finprep(
        self,
        mock_request_income_statements_finprep,
        mock_request_balance_sheets_finprep,
        mock_request_cashflow_statements_finprep,
    ):
        mock_request_income_statements_finprep.return_value = (
            "mock_request_income_statements_finprep"
        )
        mock_request_balance_sheets_finprep.return_value = (
            "mock_request_balance_sheets_finprep"
        )
        mock_request_cashflow_statements_finprep.return_value = (
            "mock_request_cashflow_statements_finprep"
        )
        self.assertEqual(
            self.parser.request_financials_finprep(self.ticker, self.dict_params),
            {
                "income_statements": "mock_request_income_statements_finprep",
                "balance_sheets": "mock_request_balance_sheets_finprep",
                "cashflow_statements": "mock_request_cashflow_statements_finprep",
            },
        )
        mock_request_income_statements_finprep.assert_called_once_with(
            self.ticker,
            self.dict_params,
        )
        mock_request_balance_sheets_finprep.assert_called_once_with(
            self.ticker,
            self.dict_params,
        )
        mock_request_cashflow_statements_finprep.assert_called_once_with(
            self.ticker,
            self.dict_params,
        )
