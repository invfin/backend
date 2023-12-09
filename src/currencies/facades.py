import logging
from datetime import date
from decimal import Decimal
from typing import Any

import requests

from src.currencies.models import ExchangeRate
from src.currencies.parse import ExchangerateHost, ExchangeRateResponse

logger = logging.getLogger(__name__)


class ExchangeRateFacade:
    def __init__(
        self,
        base: str,
        pk: int | None = None,
        target: str = "",
        target_pk: int | None = None,
        date: None | date = None,
    ) -> None:
        self.pk = pk
        self.base = base
        self.target = target
        self.date = date
        self.target_pk = target_pk

    def convert(self, amount: Decimal) -> Decimal:
        return amount  # TODO: currently doing this, once we get credits back we test it
        exchange_rate = self.get()
        return amount * exchange_rate.conversion_rate

    def get(self) -> ExchangeRate:
        try:
            exchange_rate = ExchangeRate.objects.get(
                base_id=self.pk,
                target_id=self.target_pk,
                date=self.date,
            )
        except (ValueError, ExchangeRate.DoesNotExist):
            parser = self.select_parser()
            resp = self.request(parser)
            exchange_rates = self.save_one_to_many(resp)
            exchange_rate = self._get_model(exchange_rates)
            if not exchange_rate:
                raise ValueError(f"Exchange rate missing: {vars(self)}")

        return exchange_rate

    def _get_model(self, models: None | list[ExchangeRate] = None) -> ExchangeRate | None:
        if models:
            last_model = models.pop()
            if model := next(filter(self._filter, models), None):
                # TODO: maybe refresh here if nothing is saved correctly
                return model
            last_model.refresh_from_db()
            if self._filter(last_model):
                return last_model
        return ExchangeRate.objects.filter(
            base__code=self.base,
            target__code=self.target,
            date=self.date,
        ).first()

    def _filter(self, model: ExchangeRate) -> bool:
        return model.base.code == self.base and model.target.code == self.target

    def select_parser(self) -> type[ExchangeRateResponse]:
        return ExchangerateHost

    def request(self, parser: type[ExchangeRateResponse]) -> ExchangeRateResponse:
        return parser(**self._request_rates(parser))

    def _request_rates(self, parser: type[ExchangeRateResponse]) -> Any:
        url = parser.construct_url(self.base, self.date)
        resp = requests.get(url)
        try:
            resp.raise_for_status()
            resp_json = resp.json()
            parser.validate_response(resp_json)
        except (requests.HTTPError, ValueError) as e:
            logger.error(f"url: {url} \n resp: {vars(resp)} \n error: {e}")
            raise e
        return resp_json

    def save_one_to_many(self, resp: ExchangeRateResponse) -> list[ExchangeRate]:
        rates = (
            ExchangeRate(
                date=resp.date,
                base=resp.base,
                target_id=t_id,
                conversion_rate=rate,
            )
            for t_id, rate in resp
        )
        return ExchangeRate.objects.bulk_create(rates)
