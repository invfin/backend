from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
)


class TestAverageStatementsYahooQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(
            Company,
        )
        cls.inc_st_yahooquery = DTM.create(IncomeStatementYahooQuery)
        cls.bs_yahooquery = DTM.create(BalanceSheetYahooQuery)
        cls.cf_st_yahooquery = DTM.create(CashflowStatementYahooQuery)