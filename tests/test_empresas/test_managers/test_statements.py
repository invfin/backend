from django.test import TestCase

from src.empresas.models import Company, IncomeStatement
from src.periods import constants
from tests.data.empresas import CreateStatements


class TestBaseStatementManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.statements_data = CreateStatements().create_data()

    # def test_quarterly(self, **kwargs) -> QuerySet:
    #     assert 30 == IncomeStatement.objects.all().count()
    #     return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
    #
    # def test_yearly(self, include_ttm: bool = True, **kwargs) -> QuerySet:
    #     yearly_filtered = self.filter(Q(is_ttm=include_ttm) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
    #     if yearly_filtered:
    #         return yearly_filtered
    #     else:
    #         if kwargs:
    #             return self.filter(**kwargs)
    #         else:
    #             return self.all()
    #
    # def test_yearly_exclude_ttm(self, **kwargs) -> QuerySet:
    #     return self.yearly(False, **kwargs)
