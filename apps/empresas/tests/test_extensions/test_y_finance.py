from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import (
    Company,
    IncomeStatementYFinance,
    BalanceSheetYFinance,
    CashflowStatementYFinance,
)


class TestAverageStatementsYFinance(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(
            Company,
        )
        cls.inc_st_yfinance = DTM.create(IncomeStatementYFinance)
        cls.bs_yfinance = DTM.create(BalanceSheetYFinance)
        cls.cf_st_yfinance = DTM.create(CashflowStatementYFinance)