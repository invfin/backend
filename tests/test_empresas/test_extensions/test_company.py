from django.test import TestCase
from django.db.models import QuerySet

from bfet import DjangoTestingModel

from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from src.empresas.models import Company, IncomeStatement
from src.empresas.extensions.new_company_extension import CompanyData


class TestCompanyData(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.period = DjangoTestingModel.create(Period, year=1, period=PERIOD_FOR_YEAR)
        cls.period_2 = DjangoTestingModel.create(Period, year=2, period=PERIOD_FOR_YEAR)
        cls.company = DjangoTestingModel.create(Company)
        cls.inc_statement = DjangoTestingModel.create(
            IncomeStatement,
            date=1,
            is_ttm=False,
            period=cls.period,
            company=cls.company,
        )
        cls.inc_statement_2 = DjangoTestingModel.create(
            IncomeStatement,
            date=2,
            is_ttm=False,
            period=cls.period_2,
            company=cls.company,
        )

    def test_get_statements(self):
        company_statement = CompanyData(self.company).get_statements(
            "inc_statements",
            1,
        )
        print(company_statement)
        expected_result = IncomeStatement.objects.filter(date=2)
        self.assertEqual(company_statement, expected_result)
