from __future__ import annotations

import datetime
import logging
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Generator

from django.db.models import Manager

from src.cartera.constants import InvestmentMovement
from src.cartera.models import (
    Income,
    Investment,
    NetWorth,
    Savings,
    Spendings,
)
from src.currencies.facades import ExchangeRateFacade
from src.currencies.models import Currency, UserDefaultCurrency
from src.periods.outils import FiscalDate
from src.users.models import User

logger = logging.getLogger(__name__)


class CashflowMovementFacade:
    def __init__(self, model: Income | Savings | Investment | Spendings):
        self.model = model

    def update(self, target: Currency) -> None:
        amount, converted = self._amount_converted(target)
        self.model.amount_converted = amount
        self.model.read = converted
        self.model.save(update_fields=("amount_converted", "read"))

    def _amount_converted(self, target: Currency) -> tuple[Decimal, bool]:
        amount, converted = self.model.amount, True
        if target.code != self.model.currency.code:
            try:
                amount, converted = (
                    ExchangeRateFacade(
                        base_code=self.model.currency.code,
                        base_pk=self.model.currency.pk,
                        target_code=target.code,
                        target_pk=target.pk,
                        exchange_date=self.model.date,
                    ).convert(self.model.amount),
                    True,
                )
            except ValueError as e:
                converted = False
                logger.error(f"{vars(self)} error: {str(e)}")

        return amount, converted


class CashflowMovementsAmount:
    __slots__ = "total"

    def __init__(self, total: Decimal):
        self.total = total


class CashflowMovementsAmountInvestments(CashflowMovementsAmount):
    __slots__ = "cash", "dividens_interests"

    def __init__(
        self,
        purchases: Decimal,
        funds: Decimal,
        sales: Decimal,
        dividens_interests: Decimal,
    ) -> None:
        self.dividens_interests = dividens_interests
        self.total = purchases - sales + dividens_interests
        self.cash = (funds - purchases) + sales + dividens_interests


class CashflowMovementsAmounts:
    investments: CashflowMovementsAmountInvestments
    incomes: CashflowMovementsAmount
    savings: CashflowMovementsAmount
    spendings: CashflowMovementsAmount
    equity: CashflowMovementsAmount
    __slots__ = ("incomes", "savings", "spendings", "investments", "equity")

    def __init__(self, movements: Iterable[CashflowMovementsFacade]) -> None:
        for movement in movements:
            self[movement.field] = movement.amount()
        self._update_amounts()

    def __setitem__(self, key: str, value: CashflowMovementsAmount) -> None:
        setattr(self, key, value)

    def __getitem__(self, key: str) -> Decimal:
        return getattr(self, key).total

    def _update_amounts(self):
        savings = (
            (self.incomes.total - self.spendings.total)
            + self.savings.total
            + self.investments.cash
        ) - self.investments.dividens_interests

        self.savings.total = savings
        self.equity = CashflowMovementsAmount(self.investments.total + savings)


class CashflowMovementsFacade:
    def __init__(
        self, manager: Manager, field: str, target_currency: Currency, net_worth: NetWorth
    ) -> None:
        self.manager = manager
        self.field = field
        self.target_currency = target_currency
        self.net_worth = net_worth

    def amount(self) -> CashflowMovementsAmount:
        self.update()
        final = self._query_models(self.manager)
        if self.field == "investments":
            dividens_interests = self._query_models(
                Income.objects.filter(to_substract=True)
            ).get_total()
            funds = final.filter(movement=InvestmentMovement.RECEIVE_FUND.value).get_total()
            purchases = final.filter(movement=InvestmentMovement.BUY.value).get_total()
            sales = final.filter(movement=InvestmentMovement.SELL.value).get_total()
            result = CashflowMovementsAmountInvestments(
                purchases=purchases,
                funds=funds,
                sales=sales,
                dividens_interests=dividens_interests,
            )
        else:
            result = CashflowMovementsAmount(final.get_total())
        return result

    def _query_models(self, manager: Manager):
        olders = manager.filter(net_worth__period__year__lt=self.net_worth.period.year)
        past_this_year = manager.filter(
            net_worth__period__year=self.net_worth.period.year,
            net_worth__period__period__lte=self.net_worth.period.period,
        )
        return olders | past_this_year

    def update(self) -> None:
        for model in (
            self.manager.filter(read=False, net_worth=self.net_worth)
            .prefetch_related("currency")
            .iterator(chunk_size=100)
        ):
            CashflowMovementFacade(model).update(self.target_currency)
        return None


class NetWorthFacade:
    def __init__(
        self,
        user: User | None = None,
        date: datetime.date | None = None,
        net_worth: NetWorth | None = None,
        net_worth_id: int | None = None,
    ):
        self.net_worth = net_worth or self._get_net_worth(user, date, net_worth_id)

    def _get_net_worth(
        self,
        user: User | None,
        date: datetime.date | None,
        net_worth_id: int | None = None,
    ) -> NetWorth:
        if user and date:
            return self.get(user, date)
        elif net_worth_id:
            return NetWorth.objects.get(pk=net_worth_id)
        logging.error(f"user: {vars(user)}, date: {date}")
        raise ValueError("Invalid networth")

    def get(self, user: User, date: datetime.date) -> tuple[NetWorth, bool]:
        period = FiscalDate(date).period
        net_worth, _ = NetWorth.objects.get_or_create(user=user, period=period)
        return net_worth

    @classmethod
    def update_many(cls, net_worths: Iterable[NetWorth]) -> None:
        """Update the amounts of all the networth passed

        Parameters
        ----------
        net_worths: An iterable of networth to update.
            Maybe it could be done with a simple queryset.
            Probably we'll need to first check that the movements
            have an amount in the user's default currency.

        """
        for net_worth in net_worths:
            cls(net_worth=net_worth).update()
        return None

    def update(self) -> None:
        target_currency = self._get_target_currency()
        values = CashflowMovementsAmounts(self.get_movements_by_type(target_currency))
        for field in values.__slots__:
            setattr(self.net_worth, field, values[field])
        self.net_worth.save(update_fields=values.__slots__)

    def _get_target_currency(self) -> Currency:
        try:
            return self.net_worth.user.currency.currency  # type: ignore
        except Exception:
            currency = UserDefaultCurrency.objects.create(
                user=self.net_worth.user,
                currency_id=5,
            )
            return currency.currency

    def get_movements_by_type(
        self,
        target_currency: Currency,
    ) -> Generator[CashflowMovementsFacade, Any, None]:
        return (
            CashflowMovementsFacade(manager, field, target_currency, self.net_worth)
            for manager, field in (
                (Income.objects, "incomes"),
                (Savings.objects, "savings"),
                (Spendings.objects, "spendings"),
                (Investment.objects, "investments"),
            )
        )
