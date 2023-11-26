import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

from bfet import DjangoTestingModel
from django.test import TestCase
from django.utils import timezone

from src.cartera.models import (
    Income,
    Investment,
    NetWorth,
    Spendings,
)
from src.cartera.parse_transactions_file import (
    AmountToConvert,
    BatchTransactionsToConvert,
    NetWorthFacade,
)
from src.currencies.models import Currency
from src.empresas.models.company import Company
from src.users.models import User


class TestBatchTransactionsToConvert(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User)
        cls.eur = DjangoTestingModel.create(Currency, id=5, code="EUR")
        cls.usd = DjangoTestingModel.create(Currency, code="USD")
        cls.company = DjangoTestingModel.create(Company)
        now = datetime.date(year=2008, month=2, day=1)
        net_worth = DjangoTestingModel.create(NetWorth, user=cls.user)
        cls.investment = Investment(
            currency=cls.usd,
            object=cls.company,
            movement="BUY",
            net_worth=net_worth,
            amount=Decimal("512.85"),
            user=cls.user,
            date=now,
        )
        cls.investment.save()
        cls.net_worth = net_worth

    def test_get_batch(self):
        all(
            isinstance(r, BatchTransactionsToConvert)
            for r in BatchTransactionsToConvert.get_batch(self.net_worth)
        )

    def test_amounts(self):
        for response in BatchTransactionsToConvert(
            self.net_worth.net_worth_investments  # type: ignore
        ).amounts():
            assert isinstance(response, AmountToConvert)
            assert self.investment.pk == response.pk
            assert self.investment.currency.code == response.base  # type: ignore
            assert self.investment.date == response.date
            assert self.investment.amount == response.amount


class TestNetWorth(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User)
        cls.eur = DjangoTestingModel.create(Currency, id=5, code="EUR")
        cls.usd = DjangoTestingModel.create(Currency, code="USD")
        cls.company = DjangoTestingModel.create(Company)

    @patch("src.currencies.facades.ExchangeRateFacade._request_rates")
    def test_update_amount(self, _request_rates: MagicMock):
        now = timezone.now()
        nwf = NetWorthFacade(self.user, now)
        Income(
            user=self.user,
            amount=Decimal(25312.01),
            currency=self.eur,
            net_worth=nwf.net_worth,
            date=now,
        ).save()
        Investment(
            currency=self.usd,
            object=self.company,
            movement="BUY",
            net_worth=nwf.net_worth,
            amount=Decimal(512.85),
            user=self.user,
            date=now,
        ).save()
        Investment(
            currency=self.usd,
            object=self.company,
            movement="BUY",
            net_worth=nwf.net_worth,
            amount=Decimal(512.85),
            user=self.user,
            date=now,
        ).save()
        Investment(
            currency=self.usd,
            object=self.company,
            net_worth=nwf.net_worth,
            user=self.user,
            amount=Decimal(312.71),
            movement="SELL",
            date=now,
        ).save()
        Spendings(
            user=self.user,
            currency=self.eur,
            amount=Decimal(946),
            net_worth=nwf.net_worth,
            date=now,
        ).save()
        nwf.update_amount()
