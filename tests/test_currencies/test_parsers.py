import datetime
import math
import os
from decimal import Decimal
from unittest.mock import MagicMock, patch

from bfet import DjangoTestingModel
from django.test import TestCase

from src.currencies.facades import ExchangeRateFacade
from src.currencies.models import Currency, ExchangeRate
from src.currencies.parse import ExchangerateHost

from ..data.currencies import exchangerate_host_response


class TestExchangeRateFacade(TestCase):
    def test_get(self):
        all = DjangoTestingModel.create(Currency, id=941, code="ALL")
        usd = DjangoTestingModel.create(Currency, code="USD")
        date = datetime.date(year=2008, month=2, day=1)
        expected = DjangoTestingModel.create(ExchangeRate, target=all, base=usd, date=date)
        result = ExchangeRateFacade(
            base_code="USD",
            base_pk=usd.pk,
            target_pk=all.pk,
            exchange_date=date,
        ).get()
        assert expected == result

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_get_fail(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        DjangoTestingModel.create(Currency, id=943, code="AED")
        all = DjangoTestingModel.create(Currency, id=941, code="ALL")
        DjangoTestingModel.create(Currency, id=942, code="AMD")
        usd = DjangoTestingModel.create(Currency, code="USD")
        date = datetime.date(year=2008, month=2, day=1)
        assert ExchangeRate.objects.count() == 0
        result = ExchangeRateFacade(
            base_code="USD",
            exchange_date=date,
            target_code="ALL",
        ).get()
        assert ExchangeRate.objects.count() == 6
        assert result.target == all
        assert result.base == usd
        assert result.date == date

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_request(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        DjangoTestingModel.create(Currency, id=943, code="AED")
        DjangoTestingModel.create(Currency, id=941, code="ALL")
        DjangoTestingModel.create(Currency, id=942, code="AMD")
        usd = DjangoTestingModel.create(Currency, code="USD")
        ex_rate = ExchangeRateFacade(
            base_code="USD",
            exchange_date=datetime.date(year=2008, month=2, day=1),
        )
        resp = ex_rate.request(ExchangerateHost)
        assert isinstance(resp, ExchangerateHost)
        assert resp.date == datetime.date(year=2008, month=2, day=1)
        assert resp.base == usd
        assert resp.rates == {941: 82.184524, 942: 306.810795, 943: 3.67135}

    def _assert_currency(self, base, date, target, amount):
        assert base.date == date
        assert base.base == target
        assert math.isclose(base.conversion_rate, amount, rel_tol=1e-03)

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_save_one_to_many(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        aed = DjangoTestingModel.create(Currency, id=943, code="AED")
        all_ = DjangoTestingModel.create(Currency, id=941, code="ALL")
        amd = DjangoTestingModel.create(Currency, id=942, code="AMD")
        us = DjangoTestingModel.create(Currency, code="USD")
        date = datetime.date(year=2008, month=2, day=1)
        ex_rate = ExchangeRateFacade(base_code="USD", exchange_date=date)
        resp = ExchangerateHost(**exchangerate_host_response.response)
        result = ex_rate.save_one_to_many(resp)
        assert ExchangeRate.objects.count() == len(result)
        expecteds = {941: Decimal(82.184524), 942: Decimal(306.810795), 943: Decimal(3.67135)}
        assert len(result) == 6
        for ex in result[:3]:
            self._assert_currency(ex, date, us, expecteds[ex.target.pk])

        expected = {
            943: (aed, Decimal(0.27238)),
            942: (amd, Decimal(0.00326)),
            941: (all_, Decimal(0.01217)),
        }
        for ex in result[3:]:
            target, amount = expected[ex.base.pk]
            self._assert_currency(ex, date, target, amount)

    def test_filter_codes(self):
        all = DjangoTestingModel.create(Currency, id=941, code="ALL")
        quotes = {"AED": 3.67135, "ALL": 82.184524, "AMD": 306.810795}
        usd = DjangoTestingModel.create(Currency, code="USD")
        date = datetime.date(year=2008, month=2, day=1)
        DjangoTestingModel.create(ExchangeRate, target=all, base=usd, date=date)
        result = ExchangerateHost.filter_codes(quotes, usd, date)
        assert sorted(list(result)) == ["AED", "AMD"]

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_convert(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        DjangoTestingModel.create(Currency, id=941, code="ALL")
        DjangoTestingModel.create(Currency, code="USD")
        date = datetime.date(year=2008, month=2, day=1)
        result = ExchangeRateFacade(
            base_code="USD",
            exchange_date=date,
            target_code="ALL",
        ).convert(Decimal(15))
        assert math.isclose(Decimal(1232.767), result, abs_tol=3)


class TestExchangerateHost(TestCase):
    def test_init(self):
        usd = DjangoTestingModel.create(Currency, code="USD")
        DjangoTestingModel.create(Currency, id=943, code="AED")
        DjangoTestingModel.create(Currency, id=941, code="ALL")
        DjangoTestingModel.create(Currency, id=942, code="AMD")
        result = ExchangerateHost(**exchangerate_host_response.response)
        assert result.date == datetime.date(year=2008, month=2, day=1)
        assert result.base == usd
        assert result.rates == {941: 82.184524, 942: 306.810795, 943: 3.67135}

    def test_normalize_quotes(self):
        result = ExchangerateHost.normalize_quotes(
            exchangerate_host_response.response["quotes"],
            exchangerate_host_response.response["source"],
        )
        assert result == {"AED": 3.67135, "ALL": 82.184524, "AMD": 306.810795}

    @patch.dict(os.environ, {"EXCHANGE_RATE_HOST": "mytemp"}, clear=True)
    def test_construct_url(self):
        result = ExchangerateHost.construct_url(
            exchangerate_host_response.response["source"],
            datetime.date.fromisoformat(exchangerate_host_response.response["date"]),
        )
        assert result.startswith("http://api.exchangerate.host/historical?access_key=")
        assert result.endswith("&date=2008-02-01&source=USD")
