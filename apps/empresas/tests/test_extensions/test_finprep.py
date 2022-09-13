from django.test import TestCase

from apps.bfet import ExampleModel

from apps.empresas.models import (
    Company,
    IncomeStatementFinprep,
    BalanceSheetFinprep,
    CashflowStatementFinprep,
)


class TestAverageStatementsFinprep(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = ExampleModel.create(
            Company,
        )
        cls.inc_st_finprep = ExampleModel.create(IncomeStatementFinprep)
        cls.bs_finprep = ExampleModel.create(BalanceSheetFinprep)
        cls.cf_st_finprep = ExampleModel.create(CashflowStatementFinprep)