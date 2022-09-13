from django.test import TestCase

from apps.bfet import ExampleModel

from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
)


class TestAverageStatementsYahooQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = ExampleModel.create(
            Company,
        )
        cls.inc_st_yahooquery = ExampleModel.create(IncomeStatementYahooQuery)
        cls.bs_yahooquery = ExampleModel.create(BalanceSheetYahooQuery)
        cls.cf_st_yahooquery = ExampleModel.create(CashflowStatementYahooQuery)