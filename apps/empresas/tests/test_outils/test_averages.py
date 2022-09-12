from django.test import TestCase

from apps.bfet import ExampleModel

from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    IncomeStatementYFinance,
    IncomeStatementFinprep
)


class TestAverageStatements(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = ExampleModel.create(
            Company,
        )
        cls.inc_st_finprep = ExampleModel.create(IncomeStatementFinprep, net_income=34125.2)
        cls.inc_st_yahooquery = ExampleModel.create(IncomeStatementYahooQuery, net_income=51684.56)
        cls.inc_st_yfinance = ExampleModel.create(IncomeStatementYFinance, net_income=5217.76)
