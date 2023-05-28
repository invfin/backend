from unittest.mock import MagicMock, patch

from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import (
    BalanceSheetFinprep,
    CashflowStatementFinprep,
    Company,
    IncomeStatementFinprep,
)
from src.empresas.parse.finprep import FinprepInfo


class TestFinprepInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.ticker = "AAPL"
        cls.company = DjangoTestingModel.create(Company, ticker=cls.ticker, name="Apple")
        cls.parser = FinprepInfo(cls.company)

    def test_create_statement_finprep(self):
        statement = MagicMock()
        statement_model = MagicMock()
        normalize_data = MagicMock()
        normalize_data.return_value = {
            "company": "company",
            "period": "period",
            "rest": "rest",
        }
        statement_model.objects.update_or_create = MagicMock()
        statement_model.objects.update_or_create.return_value = "update_or_create_result"
        result = self.parser.create_statement_finprep(
            [statement],
            statement_model,
            normalize_data,
        )
        statement_model.objects.update_or_create.assert_called_once_with(
            company="company",
            period="period",
            defaults={"rest": "rest"},
        )
        self.assertEqual(result, ["update_or_create_result"])

    @patch("src.empresas.parse.finprep.FinprepInfo.create_statement_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.request_income_statements_finprep")
    def test_create_income_statements_finprep(
        self,
        mock_request_income_statements_finprep,
        mock_create_statement_finprep,
    ):
        mock_request_income_statements_finprep.return_value = "income_statements_finprep"
        self.parser.create_income_statements_finprep()
        mock_request_income_statements_finprep.assert_called_once_with(self.ticker)
        mock_create_statement_finprep.assert_called_once_with(
            "income_statements_finprep",
            IncomeStatementFinprep,
            self.parser.normalize_income_statements_finprep,
        )

    @patch("src.empresas.parse.finprep.FinprepInfo.create_statement_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.request_balance_sheets_finprep")
    def test_create_balance_sheets_finprep(
        self,
        mock_request_balance_sheets_finprep,
        mock_create_statement_finprep,
    ):
        mock_request_balance_sheets_finprep.return_value = "balance_sheets_finprep"
        self.parser.create_balance_sheets_finprep()
        mock_request_balance_sheets_finprep.assert_called_once_with(self.ticker)
        mock_create_statement_finprep.assert_called_once_with(
            "balance_sheets_finprep",
            BalanceSheetFinprep,
            self.parser.normalize_balance_sheets_finprep,
        )

    @patch("src.empresas.parse.finprep.FinprepInfo.create_statement_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.request_cashflow_statements_finprep")
    def test_create_cashflow_statements_finprep(
        self,
        mock_request_cashflow_statements_finprep,
        mock_create_statement_finprep,
    ):
        mock_request_cashflow_statements_finprep.return_value = "cashflow_statements_finprep"
        self.parser.create_cashflow_statements_finprep()
        mock_request_cashflow_statements_finprep.assert_called_once_with(self.ticker)
        mock_create_statement_finprep.assert_called_once_with(
            "cashflow_statements_finprep",
            CashflowStatementFinprep,
            self.parser.normalize_cashflow_statements_finprep,
        )

    @patch("src.empresas.parse.finprep.FinprepInfo.create_cashflow_statements_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.create_balance_sheets_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.create_income_statements_finprep")
    @patch("src.empresas.parse.finprep.FinprepInfo.request_financials_finprep")
    def create_financials_finprep(
        self,
        mock_request_financials_finprep,
        mock_create_income_statements_finprep,
        mock_create_balance_sheets_finprep,
        mock_create_cashflow_statements_finprep,
    ):
        mock_request_financials_finprep.return_value = {
            "income_statements": "income_statements_finprep",
            "balance_sheets": "balance_sheets_finprep",
            "cashflow_statements": "cashflow_statements_finprep",
        }
        mock_create_income_statements_finprep.return_value = "created_income_statements"
        mock_create_balance_sheets_finprep.return_value = "created_balance_sheets"
        mock_create_cashflow_statements_finprep.return_value = "created_cashflow_statements"
        self.assertEqual(
            self.parser.create_financials_finprep(),
            {
                "income_statements": "created_income_statements",
                "balance_sheets": "created_balance_sheets",
                "cashflow_statements": "created_cashflow_statements",
            },
        )
        mock_request_financials_finprep.assert_called_once_with(self.ticker)
        mock_create_income_statements_finprep.assert_called_once_with(
            "income_statements_finprep"
        )
        mock_create_balance_sheets_finprep.assert_called_once_with("balance_sheets_finprep")
        mock_create_cashflow_statements_finprep.assert_called_once_with(
            "cashflow_statements_finprep"
        )
