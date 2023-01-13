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
        statements = CompanyData(self.company).get_statements()
        assert "inc_statements" in statements
        assert "balance_sheets" in statements
        assert "cf_statements" in statements
        assert "rentability_ratios" in statements
        assert "liquidity_ratios" in statements
        assert "margins" in statements
        assert "fcf_ratios" in statements
        assert "per_share_values" in statements
        assert "non_gaap_figures" in statements
        assert "operation_risks_ratios" in statements
        assert "ev_ratios" in statements
        assert "growth_rates" in statements
        assert "efficiency_ratios" in statements
        assert "price_to_ratios" in statements
