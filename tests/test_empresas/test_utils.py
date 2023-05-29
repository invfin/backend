from datetime import datetime, date
from unittest import skip

from django.test import TestCase
from django.utils import timezone

from bfet import DjangoTestingModel

from src.empresas.models import Company, IncomeStatementFinprep
from src.empresas.utils import FinprepRequestCheck, arrange_quarters
from src.periods.constants import PERIODS_QUARTERS
from src.periods.models import Period


class TestUtils(TestCase):
    def test_arrange_quarters(self):
        company = DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        periods = {
            period: DjangoTestingModel.create(Period, year=2021, period=period)
            for period, _ in PERIODS_QUARTERS
        }
        stt_q1 = DjangoTestingModel.create(
            IncomeStatementFinprep,
            fill_all_fields=False,
            company=company,
            period=None,
            date=None,
            year=date(2021, 2, 23),
        )
        stt_q2 = DjangoTestingModel.create(
            IncomeStatementFinprep,
            fill_all_fields=False,
            company=company,
            period=None,
            date=2021,
            year=date(2021, 4, 23),
        )
        stt_q3 = DjangoTestingModel.create(
            IncomeStatementFinprep,
            company=company,
            period=None,
            date=None,
            year=date(2021, 9, 23),
        )
        stt_q4 = DjangoTestingModel.create(
            IncomeStatementFinprep,
            fill_all_fields=False,
            company=company,
            period=None,
            date=None,
            year=date(2022, 12, 30),
        )
        arrange_quarters(company)
        self.assertEqual(stt_q1.period, periods[1])
        self.assertEqual(stt_q1.date, 2021)
        self.assertEqual(stt_q2.period, periods[2])
        self.assertEqual(stt_q2.date, 2021)
        self.assertEqual(stt_q3.period, periods[3])
        self.assertEqual(stt_q3.date, 2021)
        self.assertEqual(stt_q4.period, periods[4])
        self.assertEqual(stt_q4.date, 2022)


class TestFinprepRequestCheck(TestCase):
    def test_check_remaining_requests(self):
        yesterday = 1669368787
        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(
            120, yesterday, 30
        )
        assert is_auth is True
        assert 120 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(
            120, yesterday, 120
        )
        assert is_auth is True
        assert 120 == requests_done

        now = datetime.timestamp(timezone.now())
        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(
            120, now, 0
        )
        assert is_auth is True
        assert 120 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(
            3, now, 248
        )
        assert is_auth is False
        assert 251 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(
            20, now, 40
        )
        assert is_auth is True
        assert 60 == requests_done

    @skip("need to find how to mock the file")
    def test_manage_track_requests(self):
        assert FinprepRequestCheck().manage_track_requests(120) is True
        assert FinprepRequestCheck().manage_track_requests(30) is False
