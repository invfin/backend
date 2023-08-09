from datetime import datetime, date

from django.test import TestCase

from src.periods.outils import FiscalDate


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
