from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import Company, IncomeStatement
from src.empresas.outils.statements import StatementsData
from src.periods import constants
from src.periods.models import Period


class TestStatementsData(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.periods = []
        cls.company = DjangoTestingModel.create(Company)
        for year in [2021, 2022]:
            for period, name in constants.PERIODS:
                period_obj = DjangoTestingModel.create(
                    Period,
                    year=year,
                    period=period
                )
                DjangoTestingModel.create(
                    IncomeStatement,
                    period=period_obj,
                    company=cls.company,
                )
                cls.periods.append(period_obj)

    def get_pass(self):
        pass
