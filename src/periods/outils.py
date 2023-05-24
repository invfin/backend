from typing import Union, Dict, Optional, List
from datetime import datetime, date
from dateutil.parser import parse

from .constants import (
    PERIOD_1_QUARTER,
    PERIOD_2_QUARTER,
    PERIOD_3_QUARTER,
    PERIOD_4_QUARTER,
    QUARTER_PER_MONTH,
)
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

    @staticmethod
    def _any_date_to_date_object(regular_date: Union[str, date, datetime]) -> date:
        if type(regular_date) == str:
            regular_date = parse(
                regular_date,
                dayfirst=True,
                yearfirst=True,
            ).date()
        elif type(regular_date) == datetime:
            regular_date = regular_date.date()
        return regular_date  # type: ignore

    @staticmethod
    def _get_quarter(month: int) -> int:
        return QUARTER_PER_MONTH[month]


class FiscalYearDates:
    quarters: Dict[int, Optional[date]] = {
        PERIOD_1_QUARTER: None,
        PERIOD_2_QUARTER: None,
        PERIOD_3_QUARTER: None,
        PERIOD_4_QUARTER: None,
    }

    def __init__(self, yearly: FiscalDate, quarters: List[FiscalDate]) -> None:
        self.quarters = self.match_quarters(yearly, quarters)

    @staticmethod
    def match_quarters(
        yearly: FiscalDate, quarters: List[FiscalDate]
    ) -> Dict[int, Optional[date]]:
        pass
