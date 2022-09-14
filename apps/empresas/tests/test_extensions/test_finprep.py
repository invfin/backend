from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import (
    Company,
    IncomeStatementFinprep,
    BalanceSheetFinprep,
    CashflowStatementFinprep,
)


class TestAverageStatementsFinprep(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(
            Company,
        )
        cls.inc_st_finprep = DTM.create(IncomeStatementFinprep)
        cls.bs_finprep = DTM.create(BalanceSheetFinprep)
        cls.cf_st_finprep = DTM.create(CashflowStatementFinprep)