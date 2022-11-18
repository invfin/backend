from unittest import skip

from django.test import TestCase
from django.db.models import Q

from bfet import DjangoTestingModel

from apps.periods.constants import PERIOD_FOR_YEAR
from apps.periods.models import Period
from apps.currencies.models import Currency
from apps.empresas.extensions.as_reported import IncomeStatementAsReportedExtended
from apps.empresas.parse.parse_json import parse_json
from apps.empresas.models import (
    Company,
    IncomeStatementAsReported,
)

from tests.data.empresas.as_reported.income_statement import KFY_2022


class TestAverageStatementsAsReported(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.period = DjangoTestingModel.create(Period, year=2022, period=PERIOD_FOR_YEAR)
        cls.currency = DjangoTestingModel.create(Currency, currency="USD", symbol="$")
        parse_json(KFY_2022, "aqui", "file")
        cls.inc_st_as_rep = IncomeStatementAsReported.objects.all().first()

    def test_get_own_field_to_map(self):
        assert [
            "revenue_field",
            "cost_of_revenue_field",
            "gross_profit_field",
            "rd_expenses_field",
            "general_administrative_expenses_field",
            "selling_marketing_expenses_field",
            "sga_expenses_field",
            "other_expenses_field",
            "operating_expenses_field",
            "cost_and_expenses_field",
            "interest_expense_field",
            "depreciation_amortization_field",
            "ebitda_field",
            "operating_income_field",
            "net_total_other_income_expenses_field",
            "income_before_tax_field",
            "income_tax_expenses_field",
            "net_income_field",
            "weighted_average_shares_outstanding_field",
            "weighted_average_diluated_shares_outstanding_field",
        ] == self.inc_st_as_rep.get_own_field_to_map()

    def test_map_fields(self):
        assert 47 == self.inc_st_as_rep.fields.filter(concept__corresponding_final_item="").count()
        assert 0 == self.inc_st_as_rep.fields.filter(~Q(concept__corresponding_final_item="")).count()
        self.inc_st_as_rep.map_fields()
        assert 37 == self.inc_st_as_rep.fields.filter(concept__corresponding_final_item="").count()
        assert 10 == self.inc_st_as_rep.fields.filter(~Q(concept__corresponding_final_item="")).count()
