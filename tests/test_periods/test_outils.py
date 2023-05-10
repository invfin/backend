from datetime import datetime, date
from unittest import TestCase
from collections import namedtuple

# from django.test import TestCase

from src.periods.outils import FiscalYearDates


class TestFiscalYearDates(TestCase):
    def setUp(self) -> None:
        self.period = namedtuple("period", ["period", "year"])
        self.statement = namedtuple("statement", ["period", "year", "date"])

    def test__any_date_to_date_object(self):
        self.assertEqual(
            FiscalYearDates._any_date_to_date_object("2020/08/08"),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalYearDates._any_date_to_date_object("08-08-2020"),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalYearDates._any_date_to_date_object("08-12-2020 23:45"),
            date(2020, 12, 8),
        )
        self.assertEqual(
            FiscalYearDates._any_date_to_date_object(date(2020, 8, 8)),
            date(2020, 8, 8),
        )
        self.assertEqual(
            FiscalYearDates._any_date_to_date_object(datetime(2020, 8, 8, 10, 23, 55)),
            date(2020, 8, 8),
        )

    def test_get_quarter(self):
        self.assertEqual(FiscalYearDates(date(2020, 2, 8)).get_quarter(), 1)
        self.assertEqual(FiscalYearDates(datetime(2020, 4, 8)).get_quarter(), 2)
        self.assertEqual(FiscalYearDates(date(2020, 8, 8)).get_quarter(), 3)
        self.assertEqual(FiscalYearDates("08-12-2020 23:45").get_quarter(), 4)

    def test_arrange_quarters(self):
        q1 = self.period(2021, 1)
        q2 = self.period(2021, 2)
        q3 = self.period(2021, 3)
        q4 = self.period(2021, 4)
        fy = self.period(2021, 5)
        stt_fy = self.statement(fy, 2021, date(2021, 12, 23))
        stt_q1 = self.statement(None, 2021, date(2021, 2, 23))
        stt_q2 = self.statement(None, 2021, date(2021, 4, 23))
        stt_q3 = self.statement(None, 2021, date(2021, 9, 23))
