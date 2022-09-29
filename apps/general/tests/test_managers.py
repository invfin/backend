import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db

from bfet import DjangoTestingModel as DTM
from apps.general.models import Period
from apps.general import constants


class TestPeriodManager(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for index in range(5):
            for period in constants.PERIODS:
                DTM.create(
                    Period,
                    year=(2020+index),
                    period=period[0]
                )

    def test_for_year_period(self):
        period = Period.objects.for_year_period(2021)
        self.assertEqual(2021, period.year)
        self.assertEqual(constants.PERIOD_FOR_YEAR, period.period)

    def test_first_quarter_period(self):
        period = Period.objects.first_quarter_period(2021)
        self.assertEqual(2021, period.year)
        self.assertEqual(constants.PERIOD_1_QUARTER, period.period)

    def test_second_quarter_period(self):
        period = Period.objects.second_quarter_period(2021)
        self.assertEqual(2021, period.year)
        self.assertEqual(constants.PERIOD_2_QUARTER, period.period)

    def test_third_quarter_period(self):
        period = Period.objects.third_quarter_period(2021)
        self.assertEqual(2021, period.year)
        self.assertEqual(constants.PERIOD_3_QUARTER, period.period)
