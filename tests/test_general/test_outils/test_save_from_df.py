from unittest.mock import call, patch

from django.test import TestCase

from pandas import DataFrame

from src.general.outils.save_from_df import DFInfoCreator


class TestDFInfoCreator(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.info = DFInfoCreator()
        cls.info.income_statement_model = "income_statement_model"
        cls.info.balance_sheet_model = "balance_sheet_model"
        cls.info.cashflow_statement_model = "cashflow_statement_model"
        cls.info.normalize_income_statement = "normalize_income_statement"
        cls.info.normalize_balance_sheet = "normalize_balance_sheet"
        cls.info.normalize_cashflow_statement = "normalize_cashflow_statement"

    @patch("src.general.outils.save_from_df.DFInfoCreator.create_statement")
    def test_create_financials(self, mock_create_statement):
        self.info.create_financials("incomes_df", "balance_sheets_df", "cashflows_df", "period")
        calls = [
            call(
                "incomes_df",
                "period",
                "normalize_income_statement",
                "income_statement_model",
            ),
            call(
                "balance_sheets_df",
                "period",
                "normalize_balance_sheet",
                "balance_sheet_model",
            ),
            call(
                "cashflows_df",
                "period",
                "normalize_cashflow_statement",
                "cashflow_statement_model",
            ),
        ]
        mock_create_statement.assert_has_calls(calls)

    @patch("src.general.outils.save_from_df.DFInfoCreator.create_statements_from_df")
    def test_create_statement(self, mock_create_statements_from_df):
        self.info.create_statement(
            DataFrame(),
            "period",
            "normalizer",
            "model",
        )
        mock_create_statements_from_df.assert_called_once()

    def test_create_statements_from_df(self):
        with self.assertRaises(NotImplementedError):
            self.info.create_statements_from_df(
                "df",
                "period",
                "normalizer",
                "model",
            )
