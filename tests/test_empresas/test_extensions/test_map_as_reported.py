from django.test import TestCase

from bfet import DjangoTestingModel as dtm

from apps.periods.constants import PERIOD_FOR_YEAR
from apps.periods.models import Period
from apps.empresas.extensions.as_reported import IncomeStatementAsReportedExtended
from apps.empresas.models import (
    Company,
    IncomeStatementAsReported,
    BalanceSheetAsReported,
    CashflowStatementAsReported,
)

from tests.data.empresas.as_reported.income_statement import AAPL_2020

class TestAverageStatementsAsReported(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = dtm.create(Company)
        cls.period = dtm.create(Period, year=2020, period=PERIOD_FOR_YEAR)
        cls.inc_st_as_rep = dtm.create(IncomeStatementAsReported, company=cls.company, period=cls.period, financial_data=AAPL_2020,)

    def test_get_own_field_to_map(self):
        assert ['revenue_field', 'cost_of_revenue_field', 'gross_profit_field', 'rd_expenses_field', 'general_administrative_expenses_field', 'selling_marketing_expenses_field', 'sga_expenses_field', 'other_expenses_field', 'operating_expenses_field', 'cost_and_expenses_field', 'interest_expense_field', 'depreciation_amortization_field', 'ebitda_field', 'operating_income_field', 'net_total_other_income_expenses_field', 'income_before_tax_field', 'income_tax_expenses_field', 'net_income_field', 'weighted_average_shares_outstanding_field', 'weighted_average_diluated_shares_outstanding_field',] == self.inc_st_as_rep.get_own_field_to_map()

    def test_map_fields(self):
        pass
