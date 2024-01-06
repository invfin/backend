import datetime
import math
from decimal import Decimal
from unittest.mock import MagicMock, patch
from bfet import DjangoTestingModel

from model_bakery import baker
from django.test import TestCase

from src.cartera.models import (
    Income,
    NetWorth,
    Spendings,
)
from src.cartera.facades import (
    CashflowMovementFacade,
    CashflowMovementsFacade,
)
from src.cartera.parse_transactions_file import (
    NetWorthFacade,
)
from src.currencies.models import Currency, ExchangeRate, UserDefaultCurrency
from src.users.models import User

from ..data.currencies import exchangerate_host_response


class TestCashflowMovementFacade(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make(User)
        cls.eur = baker.make(Currency, id=5, code="EUR")
        cls.usd = baker.make(Currency, code="USD")
        cls.date = datetime.date(year=2008, month=2, day=1)
        baker.make(
            ExchangeRate,
            base=cls.usd,
            target=cls.eur,
            conversion_rate=Decimal("0.91"),
            date=cls.date,
        )

    def test_update(self):
        income = baker.make(
            Income,
            currency=self.usd,
            amount=Decimal("100"),
            date=self.date,
        )
        CashflowMovementFacade(income).update(self.eur)
        assert income.amount_converted == Decimal("91.000")
        assert income.read

    def test_amount_converted(self):
        income = baker.make(
            Income,
            currency=self.usd,
            amount=Decimal("100"),
            date=self.date,
        )
        amount, converted = CashflowMovementFacade(income)._amount_converted(self.eur)
        assert amount == Decimal("91.000")
        assert converted


class TestCashflowMovementsFacade(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make(User)
        cls.eur = baker.make(Currency, id=5, code="EUR")
        cls.usd = baker.make(Currency, code="USD")
        cls.date = datetime.date(year=2008, month=2, day=1)
        baker.make(
            ExchangeRate,
            base=cls.usd,
            target=cls.eur,
            conversion_rate=Decimal("0.91"),
            date=cls.date,
        )
        cls.net_worth = baker.make(NetWorth, user=cls.user)
        baker.make(
            Income,
            currency=cls.usd,
            net_worth=cls.net_worth,
            amount=Decimal("100"),
            user=cls.user,
            date=cls.date,
            read=True,
            amount_converted=Decimal("91"),
        )

    def test_total_amount(self):
        baker.make(
            Income,
            currency=self.usd,
            net_worth=self.net_worth,
            amount=Decimal("100"),
            user=self.user,
            date=self.date,
            read=False,
        )
        result = CashflowMovementsFacade(
            self.net_worth.net_worth_incomes,
            "incomes",
            self.eur,
        ).total_amount()
        self.assertEqual(result, Decimal("182.000"))

    def test_update(self):
        income = baker.make(
            Income,
            currency=self.usd,
            net_worth=self.net_worth,
            amount=Decimal("100"),
            user=self.user,
            date=self.date,
            read=False,
        )
        CashflowMovementsFacade(
            self.net_worth.net_worth_incomes,
            "incomes",
            self.eur,
        ).update()
        income.refresh_from_db()
        assert income.amount_converted == Decimal("91.000")
        assert income.read


class TestNetWorthFacade(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make(User)
        cls.usd = baker.make(Currency, id=5, code="USD")
        cls.amd = baker.make(Currency, code="AMD")
        cls.all = baker.make(Currency, code="ALL")
        cls.aed = baker.make(Currency, code="AED")

    def test_get_target_currency(self):
        date = datetime.date(year=2008, month=2, day=1)
        result = NetWorthFacade(user=self.user, date=date)._get_target_currency()
        self.assertEqual(result, self.usd)

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_update(self, _request_rates: MagicMock):
        _request_rates.side_effect = (
            exchangerate_host_response.update_response_quotes("AMD"),
            exchangerate_host_response.update_response_quotes("ALL"),
        )
        date = datetime.date(year=2008, month=2, day=1)
        UserDefaultCurrency.objects.create(user=self.user, currency=self.usd)
        nwf = NetWorthFacade(self.user, date)
        assert ExchangeRate.objects.count() == 0
        income = DjangoTestingModel.create(
            Income,
            user=self.user,
            amount=Decimal(445612.01),
            currency=self.amd,
            net_worth=nwf.net_worth,
            date=date,
            read=False,
        )
        spending = DjangoTestingModel.create(
            Spendings,
            user=self.user,
            currency=self.all,
            amount=Decimal(94565.45),
            net_worth=nwf.net_worth,
            date=date,
            read=False,
        )
        nwf.update()
        income.refresh_from_db()
        spending.refresh_from_db()
        assert ExchangeRate.objects.count() == 10
        assert math.isclose(income.amount_converted, Decimal(1452.400), abs_tol=3)
        assert math.isclose(spending.amount_converted, Decimal(1150.648), abs_tol=3)
        assert math.isclose(nwf.net_worth.equity, Decimal(301.752), abs_tol=3)
        assert math.isclose(nwf.net_worth.incomes, Decimal(1452.400), abs_tol=3)
        assert math.isclose(nwf.net_worth.spendings, Decimal(1150.648), abs_tol=3)
        assert math.isclose(nwf.net_worth.savings, Decimal(301.752), abs_tol=3)
