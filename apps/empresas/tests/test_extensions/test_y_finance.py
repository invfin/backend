from django.test import TestCase

from apps.bfet import ExampleModel

from apps.empresas.models import (
    Company,
    IncomeStatementYFinance,
    BalanceSheetYFinance,
    CashflowStatementYFinance,
)


class TestAverageStatementsYFinance(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = ExampleModel.create(
            Company,
        )
        cls.inc_st_yfinance = ExampleModel.create(IncomeStatementYFinance)
        cls.bs_yfinance = ExampleModel.create(BalanceSheetYFinance)
        cls.cf_st_yfinance = ExampleModel.create(CashflowStatementYFinance)