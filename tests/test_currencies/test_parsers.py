import datetime
from unittest.mock import MagicMock, patch

from django.test import TestCase

from src.currencies.facades import ExchangeRateFacade
from src.currencies.models import ExchangeRate
from src.currencies.parse import ExchangerateHost

from ..data.currencies import exchangerate_host_response


class TestExchangeRateFacade(TestCase):
    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_request(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        ex_rate = ExchangeRateFacade(base="USD", date=datetime.date(year=2008, month=2, day=1))
        resp = ex_rate.request(ExchangerateHost)
        assert isinstance(resp, ExchangerateHost)

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_get(self, _request_rates: MagicMock):
        _request_rates.return_value = exchangerate_host_response.response
        date = datetime.date(year=2008, month=2, day=1)
        ex_rate = ExchangeRateFacade(base="USD", date=date)
        assert ExchangeRate.objects.count() == 0
        resp = ex_rate.get()
        assert isinstance(resp, ExchangeRate)
        assert resp.date == date
        assert resp.currency.code == "USD"
        assert ExchangeRate.objects.count() == 157
