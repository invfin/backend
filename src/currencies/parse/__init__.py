import datetime
import logging
from collections.abc import Generator
from decimal import Decimal
from typing import Any

from django.conf import settings

from src.currencies.models import Currency, ExchangeRate

logger = logging.getLogger(__name__)


class ExchangeRateResponse:
    date: datetime.date
    base: Currency
    rates: dict[int, float]

    def __iter__(self) -> Generator[tuple[int, Decimal], None, None]:
        for currency, rate in self.rates.items():
            yield currency, Decimal(rate)

    @classmethod
    def get_currency(cls, code: str) -> Currency:
        currency, _ = Currency.objects.get_or_create(code=code)
        return currency

    @classmethod
    def get_rates(
        cls,
        conversion_rates: dict[str, float],
        base: Currency,
        date: datetime.date,
    ) -> dict[int, float]:
        codes = cls.filter_codes(conversion_rates, base, date)
        return {cls.get_currency(s).pk: conversion_rates[s] for s in codes}

    @classmethod
    def filter_codes(
        cls,
        conversion_rates: dict[str, float],
        base: Currency,
        date: datetime.date,
    ) -> set[str]:
        existing = ExchangeRate.objects.filter(
            target__code__in=conversion_rates.keys(),
            base=base,
            date=date,
        ).values_list("target__code", flat=True)
        return set(conversion_rates.keys()) - set(existing)

    @classmethod
    def construct_url(cls, *_, **__) -> str:
        ...

    @classmethod
    def validate_response(cls, *_, **__):
        ...


class ExchangerateAPI(ExchangeRateResponse):
    """
    https://v6.exchangerate-api.com
    """

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        base_code: str,
        conversion_rates: dict[str, float],
        **_,
    ):
        date_instance = datetime.date(year=year, month=month, day=day)
        base = self.get_currency(base_code)
        rates = self.get_rates(
            conversion_rates,
            base,
            date_instance,
        )
        self.date = date_instance
        self.base = base
        self.rates = rates

    @classmethod
    def validate_response(cls, response: Any):
        if response["result"] == "error":
            raise ValueError(response["error-type"])

    @classmethod
    def construct_url(
        cls,
        base: str,
        target: str = "",
        date: None | datetime.date = None,
        amount: Decimal | None = None,
    ) -> str:
        amount_path = f"/{amount}" if amount else ""
        final_path = ""

        if date:
            date_path = date.strftime("/%Y/%-m/%-d")
            final_path = f"history/{base}{date_path}{amount_path}"
        elif target:
            final_path = f"pair/{base}/{target}{amount_path}"
        if not final_path:
            logger.error(
                f"base: {base} \n target: {target} \n date: {date} \n amount: {amount}"
            )
            raise ValueError(f"No final path in {cls.__name__}")
        base_url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE}"
        return f"{base_url}/{final_path}"


class ExchangerateHost(ExchangeRateResponse):
    """
    exchangerate.host
    """

    def __init__(self, date: str, source: str, quotes: dict[str, float], **_):
        date_instance = datetime.date.fromisoformat(date)
        base = self.get_currency(source)
        rates = self.get_rates(
            self.normalize_quotes(quotes, source),
            base,
            date_instance,
        )
        self.date = date_instance
        self.base = base
        self.rates = rates

    @classmethod
    def normalize_quotes(cls, quotes: dict[str, float], source: str) -> dict[str, float]:
        return {k.replace(source, ""): v for k, v in quotes.items()}

    @classmethod
    def validate_response(cls, response: Any):
        if not response["success"]:
            raise ValueError(response)

    @classmethod
    def construct_url(cls, source: str, date: datetime.date) -> str:
        base_path = "http://api.exchangerate.host/historical"
        date_query = f"&date={date.strftime('%Y-%m-%d')}"
        source_query = f"&source={source}"
        acces_query = f"access_key={settings.EXCHANGE_RATE_HOST}"
        return f"{base_path}?{acces_query}{date_query}{source_query}"
