from __future__ import annotations
from typing import Union
from datetime import datetime, date
from dateutil.parser import parse

from django.utils import timezone

from .constants import QUARTER_PER_MONTH
from .models import Period


class FiscalDate:
    regular_date: date
    fiscal_quarter: int
    period: Period

    def __init__(self, regular_date: Union[str, date, datetime]) -> None:
        date_object = self._any_date_to_date_object(regular_date)
        quarter = self._get_quarter(date_object.month)
        period, _ = Period.objects.get_or_create(year=date_object.year, period=quarter)
        self.regular_date = date_object
        self.fiscal_quarter = quarter
        self.period = period

    @classmethod
    def current(cls) -> FiscalDate:
        return cls(timezone.now())

    @staticmethod
    def _any_date_to_date_object(regular_date: Union[str, date, datetime]) -> date:
        if isinstance(regular_date, str):
            regular_date = parse(
                regular_date,
                dayfirst=True,
                yearfirst=True,
            ).date()
        elif isinstance(regular_date, datetime):
            regular_date = regular_date.date()
        return regular_date  # type: ignore

    @staticmethod
    def _get_quarter(month: int) -> int:
        return QUARTER_PER_MONTH[month]
