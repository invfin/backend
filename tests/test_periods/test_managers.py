from django.test import TestCase

from bfet import DjangoTestingModel
from apps.periods.models import Period
from apps.periods import constants


class TestPeriodManager(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for index in range(5):
            for period in constants.PERIODS:
                DjangoTestingModel.create(Period, year=(2020 + index), period=period[0])

    def test_for_year_period(self):
        period = Period.objects.for_year_period(2021)
        assert 2021 == period.year
        assert constants.PERIOD_FOR_YEAR == period.period

    def test_first_quarter_period(self):
        period = Period.objects.first_quarter_period(2021)
        assert 2021 == period.year
        assert constants.PERIOD_1_QUARTER == period.period

    def test_second_quarter_period(self):
        period = Period.objects.second_quarter_period(2021)
        assert 2021 == period.year
        assert constants.PERIOD_2_QUARTER == period.period

    def test_third_quarter_period(self):
        period = Period.objects.third_quarter_period(2021)
        assert 2021 == period.year
        assert constants.PERIOD_3_QUARTER == period.period

    def test_fourth_quarter_period(self):
        period = Period.objects.fourth_quarter_period(2021)
        assert 2021 == period.year
        assert constants.PERIOD_4_QUARTER == period.period

