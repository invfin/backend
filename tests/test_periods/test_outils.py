from datetime import datetime, date
from collections import namedtuple

from django.test import TestCase

from bfet import DjangoTestingModel

from src.periods import constants
from src.periods.models import Period
from src.periods.outils import FiscalYearDates, FiscalDate


class TestFiscalDate(TestCase):
    def test__any_date_to_date_object(self):
        self.assertEqual(
            FiscalDate._any_date_to_date_object("2020/08/08"),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalDate._any_date_to_date_object("08-08-2020"),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalDate._any_date_to_date_object("08-12-2020 23:45"),
            date(2020, 12, 8),
        )
        self.assertEqual(
            FiscalDate._any_date_to_date_object(date(2020, 8, 8)),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalDate._any_date_to_date_object(datetime(2020, 8, 8, 10, 23, 55)),
            date(2020, 8, 8),
        )

    def test_get_quarter(self):
        self.assertEqual(FiscalDate._get_quarter(2), 1)
        self.assertEqual(FiscalDate._get_quarter(4), 2)
        self.assertEqual(FiscalDate._get_quarter(8), 3)
        self.assertEqual(FiscalDate._get_quarter(12), 4)


class TestFiscalYearDates(TestCase):
    def setUp(self) -> None:
        self.statement = namedtuple("statement", ["period", "year", "date"])

    def test_arrange_quarters(self):
        for period, _ in constants.PERIODS_QUARTERS:
            DjangoTestingModel.create(Period, year=2021, period=period)
        fy = DjangoTestingModel.create(Period, year=2021, period=constants.PERIOD_FOR_YEAR)
        stt_fy = self.statement(fy, 2021, date(2021, 12, 23))
        stt_q1 = self.statement(None, 2021, date(2021, 2, 23))
        stt_q2 = self.statement(None, 2021, date(2021, 4, 23))
        stt_q3 = self.statement(None, 2021, date(2021, 9, 23))
        stt_q3 = self.statement(None, 2021, date(2021, 12, 30))
