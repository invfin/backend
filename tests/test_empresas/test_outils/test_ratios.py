from django.test import TestCase

from bfet import DjangoTestingModel, DataCreator

from apps.periods.constants import PERIOD_FOR_YEAR
from apps.currencies.models import Currency
from apps.periods.models import Period
from apps.empresas.outils.ratios import CalculateFinancialRatios
from apps.empresas.models import (
    Company,
)


class TestCalculateFinancialRatios(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
