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
        base_code: str,
        base_pk: int | None = None,
        target_code: str = "",
        target_pk: int | None = None,
        exchange_date: None | date = None,
    ) -> None:
        self.base_pk = base_pk
        self.base_code = base_code
        self.target_code = target_code
        self.date = exchange_date
        self.target_pk = target_pk

    def convert(self, amount: Decimal) -> Decimal:
        return amount * self.get().conversion_rate

    def query(self):
        query = {"base__code": self.base_code}
        if self.base_pk:
            query |= {"base_id": self.base_pk}
        if self.date:
            query |= {"date": self.date}
        if self.target_pk:
            query |= {"target_id": self.target_pk}
        if self.target_code:
            query |= {"target__code": self.target_code}
        return query

    def get(self) -> ExchangeRate:
        if exchange_rate := ExchangeRate.objects.filter(**self.query()).first():
            return exchange_rate
        parser = self.select_parser()
        resp = self.request(parser)
        exchange_rates = self.save_one_to_many(resp)
        exchange_rate = self._get_model(exchange_rates)
        if not exchange_rate:
            raise ValueError(f"Exchange rate missing: {vars(self)}")
        return exchange_rate

    def _get_model(self, models: None | list[ExchangeRate] = None) -> ExchangeRate | None:
        if models:
            if model := next(filter(self._filter, models), None):
                return model
        return ExchangeRate.objects.filter(**self.query()).first()

    def _filter(self, model: ExchangeRate) -> bool:
        # model.refresh_from_db()
        return model.base.code == self.base_code and model.target.code == self.target_code

    def select_parser(self) -> type[ExchangeRateResponse]:
        return ExchangerateHost

    def request(self, parser: type[ExchangeRateResponse]) -> ExchangeRateResponse:
        return parser(**self._request_rates(parser))

    def _request_rates(self, parser: type[ExchangeRateResponse]) -> Any:
        url = parser.construct_url(self.base_code, self.date)
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
        rates = [
            ExchangeRate(
                date=resp.date,
                base=resp.base,
                target_id=t_id,
                conversion_rate=rate,
            )
            for t_id, rate in resp
        ]
        reverse_rates = [
            ExchangeRate(
                date=resp.date,
                target=resp.base,
                base_id=t_id,
                conversion_rate=Decimal(1) / rate,
            )
            for t_id, rate in resp
        ]
        return ExchangeRate.objects.bulk_create(rates + reverse_rates, ignore_conflicts=True)
