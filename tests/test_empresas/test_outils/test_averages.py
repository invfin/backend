from unittest.mock import patch
from collections import defaultdict

from django.test import TestCase
from bfet import DjangoTestingModel

from src.currencies.models import Currency
from src.empresas.models import (
    Company,
    IncomeStatementFinprep,
    IncomeStatementYahooQuery,
)
from src.empresas.outils.data_management.update.average_statements import AverageStatements
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period


class TestAverageStatements(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DjangoTestingModel.create(Company)
        cls.period = DjangoTestingModel.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.currency = DjangoTestingModel.create(Currency)
        cls.revenue = 13929.27
        cls.cost_of_revenue = 9046.54
        cls.gross_profit = 586.94
        cls.research_and_development_expenses = 153.4
        cls.selling_general_and_administrative_expenses = 1539.07
        cls.inc_st_finprep = DjangoTestingModel.create(
            IncomeStatementFinprep,
            fill_all_fields=False,
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
            fill_all_fields=False,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            total_revenue=cls.revenue,
            reconciled_cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_and_development=cls.research_and_development_expenses,
            selling_general_and_administration=cls.selling_general_and_administrative_expenses,
        )

    def test_calculate_average_income_statement(self):
        average = AverageStatements(self.company).calculate_average_income_statement(
            self.period
        )
        assert type(average) == dict
        assert self.revenue == average["revenue"]
        assert self.cost_of_revenue == average["cost_of_revenue"]
        assert self.gross_profit == average["gross_profit"]
        assert self.research_and_development_expenses == average["rd_expenses"]
        assert self.selling_general_and_administrative_expenses == average["sga_expenses"]
        assert self.period.id == average["period_id"]
        assert self.period.year == average["date"]
        assert self.currency.id == average["reported_currency_id"]

    def test_return_averaged_data(self):
        statements = [
            self.company.incomestatementfinprep_set.filter(period=self.period).first(),
            self.company.incomestatementyfinance_set.filter(period=self.period).first(),
            self.company.incomestatementyahooquery_set.filter(period=self.period).first(),
        ]
        self.assertEqual(
            AverageStatements.return_averaged_data(self.period, statements),
            {
                "cost_of_revenue": 9046.54,
                "date": 2021,
                "gross_profit": 586.94,
                "period_id": self.period.id,
                "rd_expenses": 153.4,
                "reported_currency_id": self.currency.id,
                "revenue": 13929.27,
                "sga_expenses": 1539.07,
            },
        )

    @patch("src.empresas.outils.average_statements.AverageStatements.prepare_data")
    @patch("src.empresas.outils.average_statements.AverageStatements.find_correct_currency")
    @patch("src.empresas.outils.average_statements.AverageStatements.calculate_averages")
    def test_return_averaged_data_patched(
        self,
        mock_calculate_averages,
        mock_find_correct_currency,
        mock_prepare_data,
    ):
        mock_prepare_data.return_value = {"net_income": 5}
        mock_find_correct_currency.return_value = {"reported_currency_id": 5}
        mock_calculate_averages.return_value = {"gross_profit": 5, "net_income": 5}
        self.assertEqual(
            AverageStatements.return_averaged_data(self.period, []),
            {
                "date": self.period.year,
                "period_id": self.period.id,
                "reported_currency_id": 5,
                "net_income": 5,
                "gross_profit": 5,
            },
        )
        mock_prepare_data.assert_called_once_with([])
        mock_find_correct_currency.assert_called_once_with({"net_income": 5})
        mock_calculate_averages.assert_called_once_with({"net_income": 5})

    @patch("src.empresas.outils.average_statements.AverageStatements.prepare_data")
    @patch("src.empresas.outils.average_statements.AverageStatements.find_correct_currency")
    @patch("src.empresas.outils.average_statements.AverageStatements.calculate_averages")
    def test_return_averaged_data_empty(
        self,
        mock_calculate_averages,
        mock_find_correct_currency,
        mock_prepare_data,
    ):
        mock_prepare_data.return_value = defaultdict(list)
        self.assertIsNone(AverageStatements.return_averaged_data(self.period, []))
        mock_prepare_data.assert_called_once_with([])
        mock_find_correct_currency.assert_not_called()
        mock_calculate_averages.assert_not_called()

    def test_prepare_data(self):
        result = AverageStatements.prepare_data(
            [
                self.company.incomestatementfinprep_set.filter(period=self.period).first(),
                self.company.incomestatementyfinance_set.filter(period=self.period).first(),
                self.company.incomestatementyahooquery_set.filter(period=self.period).first(),
            ]
        )
        expected = defaultdict(
            list,
            revenue=[self.revenue, self.revenue],
            cost_of_revenue=[self.cost_of_revenue, self.cost_of_revenue],
            gross_profit=[self.gross_profit, self.gross_profit],
            rd_expenses=[
                self.research_and_development_expenses,
                self.research_and_development_expenses,
            ],
            sga_expenses=[
                self.selling_general_and_administrative_expenses,
                self.selling_general_and_administrative_expenses,
            ],
            reported_currency_id=[self.currency.id, self.currency.id],
        )
        self.assertEqual(result, expected)

    def test_prepare_data_empty(self):
        self.assertEqual(AverageStatements.prepare_data([]), {})

    def test_find_correct_currency(self):
        result = AverageStatements.find_correct_currency(
            defaultdict(reported_currency_id=[1, 3, 5, 1], hey=[1, 2]),
        )
        self.assertEqual(
            result,
            {"reported_currency_id": 1},
        )

    def test_find_correct_currency_empty(self):
        self.assertEqual(
            AverageStatements.find_correct_currency(defaultdict(hey=[1, 2])),
            {"reported_currency_id": None},
        )

    def test_calculate_averages(self):
        data = defaultdict(net_income=[5, 5, 6], cash=[6, 3, 4])
        self.assertEqual(
            AverageStatements.calculate_averages(data),
            {"net_income": 5.33, "cash": 4.33},
        )
