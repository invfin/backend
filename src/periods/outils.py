from typing import Union
from datetime import datetime, date
from dateutil.parser import parse

from .constants import (
    PERIOD_1_QUARTER,
    PERIOD_2_QUARTER,
    PERIOD_3_QUARTER,
    PERIOD_4_QUARTER,
)


class FiscalYearDates:
    regular_date: date
    fiscal_first_quarter: tuple[set[int], int] = (
        {1, 2, 3},
        PERIOD_1_QUARTER,
    )
    fiscal_second_quarter: tuple[set[int], int] = (
        {4, 5, 6},
        PERIOD_2_QUARTER,
    )
    fiscal_third_quarter: tuple[set[int], int] = (
        {7, 8, 9},
        PERIOD_3_QUARTER,
    )
    fiscal_fourth_quarter: tuple[set[int], int] = (
        {10, 11, 12},
        PERIOD_4_QUARTER,
    )

    def __init__(self, regular_date: Union[str, date, datetime]) -> None:
        self.regular_date = self._any_date_to_date_object(regular_date)

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

    def get_quarter(self) -> int:  # type: ignore
        for period in [
            self.fiscal_first_quarter,
            self.fiscal_second_quarter,
            self.fiscal_third_quarter,
            self.fiscal_fourth_quarter,
        ]:
            period_range, period_num = period
            if self.regular_date.month in period_range:
                return period_num
