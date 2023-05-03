from django.test import TestCase

from unittest.mock import patch

from bfet import DjangoTestingModel, create_random_float

from src.currencies.models import Currency
from src.empresas.models import (
    BalanceSheet,
    BalanceSheetFinprep,
    BalanceSheetYahooQuery,
    BalanceSheetYFinance,
    CashflowStatement,
    CashflowStatementFinprep,
    CashflowStatementYahooQuery,
    CashflowStatementYFinance,
    Company,
    IncomeStatement,
    IncomeStatementFinprep,
    IncomeStatementYahooQuery,
    IncomeStatementYFinance,
)
from src.empresas.outils.update import UpdateCompany
from src.periods import constants
from src.periods.models import Period


class TestUpdateCompany(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DjangoTestingModel.create(
            Company,
            ticker="INTC",
            name="Intel",
        )
        cls.period = DjangoTestingModel.create(
            Period,
            year=2021,
            period=constants.PERIOD_FOR_YEAR,
        )
        cls.currency = DjangoTestingModel.create(Currency)
        cls.revenue = create_random_float()
        cls.cost_of_revenue = create_random_float()
        cls.gross_profit = create_random_float()
        cls.research_and_development_expenses = create_random_float()
        cls.selling_general_and_administrative_expenses = create_random_float()
        cls.inc_st_finprep = DjangoTestingModel.create(
            IncomeStatementFinprep,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            revenue=cls.revenue,
            cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_and_development_expenses=cls.research_and_development_expenses,
            selling_general_and_administrative_expenses=cls.selling_general_and_administrative_expenses,
        )
        cls.inc_st_yahooquery = DjangoTestingModel.create(
            IncomeStatementYahooQuery,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            total_revenue=cls.revenue,
            reconciled_cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_and_development=cls.research_and_development_expenses,
            selling_general_and_administration=cls.selling_general_and_administrative_expenses,
        )
        cls.inc_st_yfinance = DjangoTestingModel.create(
            IncomeStatementYFinance,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            total_revenue=cls.revenue,
            cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_development=cls.research_and_development_expenses,
            selling_general_administrative=cls.selling_general_and_administrative_expenses,
        )
        cls.bs_finprep = DjangoTestingModel.create(
            BalanceSheetFinprep,
            company=cls.company,
            period=cls.period,
        )
        cls.bs_yahooquery = (
            DjangoTestingModel.create(
                BalanceSheetYahooQuery,
                company=cls.company,
                period=cls.period,
            ),
        )
        cls.bs_yfinance = DjangoTestingModel.create(
            BalanceSheetYFinance,
            company=cls.company,
            period=cls.period,
        )
        cls.cf_st_finprep = DjangoTestingModel.create(
            CashflowStatementFinprep,
            company=cls.company,
            period=cls.period,
        )
        cls.cf_st_yahooquery = DjangoTestingModel.create(
            CashflowStatementYahooQuery,
            company=cls.company,
            period=cls.period,
        )
        cls.cf_st_yfinance = DjangoTestingModel.create(
            CashflowStatementYFinance,
            company=cls.company,
            period=cls.period,
        )

    def test_update_average_financials_statements(self):
        self.assertEqual(IncomeStatement.objects.all().count(), 0)
        self.assertEqual(BalanceSheet.objects.all().count(), 0)
        self.assertEqual(CashflowStatement.objects.all().count(), 0)
        UpdateCompany(self.company).update_average_financials_statements(self.period)
        self.assertEqual(IncomeStatement.objects.all().count(), 1)
        self.assertEqual(BalanceSheet.objects.all().count(), 1)
        self.assertEqual(CashflowStatement.objects.all().count(), 1)

    @patch(
        "src.empresas.outils.average_statements.AverageStatements.calculate_average_income_statement"
    )
    @patch(
        "src.empresas.outils.average_statements.AverageStatements.calculate_average_balance_sheet"
    )
    @patch(
        "src.empresas.outils.average_statements.AverageStatements.calculate_average_cashflow_statement"
    )
    @patch("empresas.outils.update.UpdateCompany.create_or_update_inc_statements")
    @patch("empresas.outils.update.UpdateCompany.create_or_update_balance_sheets")
    @patch("empresas.outils.update.UpdateCompany.create_or_update_cf_statements")
    def test_update_average_financials_statements_mocked(
        self,
        mock_create_or_update_cf_statements,
        mock_create_or_update_balance_sheets,
        mock_create_or_update_inc_statements,
        mock_calculate_average_cashflow_statement,
        mock_calculate_average_balance_sheet,
        mock_calculate_average_income_statement,
    ):
        UpdateCompany(self.company).update_average_financials_statements(self.period)
        mock_calculate_average_cashflow_statement.return_value = {
            "calculate_average_cashflow_statement": "calculate_average_cashflow_statement"
        }
        mock_calculate_average_balance_sheet.return_value = {
            "calculate_average_balance_sheet": "calculate_average_balance_sheet"
        }
        mock_calculate_average_income_statement.return_value = {
            "calculate_average_income_statement": "calculate_average_income_statement"
        }
        mock_calculate_average_cashflow_statement.assert_called_once_with(self.period)
        mock_calculate_average_balance_sheet.assert_called_once_with(self.period)
        mock_calculate_average_income_statement.assert_called_once_with(self.period)
        mock_create_or_update_cf_statements.assert_called_once_with(
            {
                "company": self.company,
                "from_average": True,
                "calculate_average_cashflow_statement": "calculate_average_cashflow_statement",
            },
            self.period,
        )
        mock_create_or_update_balance_sheets.assert_called_once_with(
            {
                "company": self.company,
                "from_average": True,
                "calculate_average_balance_sheet": "calculate_average_balance_sheet",
            },
            self.period,
        )
        mock_create_or_update_inc_statements.assert_called_once_with(
            {
                "company": self.company,
                "from_average": True,
                "calculate_average_income_statement": "calculate_average_income_statement",
            },
            self.period,
        )

    def test_create_or_update_ttm(self):
        self.assertEqual(IncomeStatement.objects.filter(is_ttm=True).count(), 0)
        self.assertEqual(BalanceSheet.objects.filter(is_ttm=True).count(), 0)
        self.assertEqual(CashflowStatement.objects.filter(is_ttm=True).count(), 0)
        periods = [
            DjangoTestingModel.create(Period, year=2021, period=constants.PERIOD_2_QUARTER),
            DjangoTestingModel.create(Period, year=2021, period=constants.PERIOD_3_QUARTER),
            DjangoTestingModel.create(Period, year=2021, period=constants.PERIOD_4_QUARTER),
            DjangoTestingModel.create(Period, year=2022, period=constants.PERIOD_1_QUARTER),
        ]
        for period in periods:
            DjangoTestingModel.create(
                IncomeStatement,
                reported_currency=self.currency,
                company=self.company,
                period=period,
                date=period.year,
                is_ttm=False,
            )
            DjangoTestingModel.create(
                BalanceSheet,
                reported_currency=self.currency,
                company=self.company,
                period=period,
                date=period.year,
                is_ttm=False,
            )
            DjangoTestingModel.create(
                CashflowStatement,
                reported_currency=self.currency,
                company=self.company,
                period=period,
                date=period.year,
                is_ttm=False,
            )
        UpdateCompany(self.company).create_or_update_ttm()
        self.assertEqual(IncomeStatement.objects.filter(is_ttm=True).count(), 1)
        self.assertEqual(BalanceSheet.objects.filter(is_ttm=True).count(), 1)
        self.assertEqual(CashflowStatement.objects.filter(is_ttm=True).count(), 1)
