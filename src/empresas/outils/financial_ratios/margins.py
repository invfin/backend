from typing import Union

from .utils import divide_or_zero, modify_for_percentage


class Margins:
    @classmethod
    def calculate_gross_margin(
        cls,
        gross_profit: Union[int, float],
        revenue: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(gross_profit, revenue)
        return modify_for_percentage(result)

    @classmethod
    def calculate_ebitda_margin(
        cls,
        ebitda: Union[int, float],
        revenue: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(ebitda, revenue)
        return modify_for_percentage(result)

    @classmethod
    def calculate_net_income_margin(
        cls,
        net_income: Union[int, float],
        revenue: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(net_income, revenue)
        return modify_for_percentage(result)

    @classmethod
    def calculate_fcf_margin(
        cls,
        free_cash_flow: Union[int, float],
        revenue: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(free_cash_flow, revenue)
        return modify_for_percentage(result)

    @classmethod
    def calculate_fcf_equity_to_net_income(
        cls,
        fcf_equity: Union[int, float],
        net_income: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(fcf_equity, net_income)
        return modify_for_percentage(result)

    @classmethod
    def calculate_unlevered_fcf_to_net_income(
        cls,
        unlevered_fcf: Union[int, float],
        net_income: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(unlevered_fcf, net_income)
        return modify_for_percentage(result)

    @classmethod
    def calculate_unlevered_fcf_ebit_to_net_income(
        cls,
        unlevered_fcf_ebit: Union[int, float],
        net_income: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(unlevered_fcf_ebit, net_income)
        return modify_for_percentage(result)

    @classmethod
    def calculate_owners_earnings_to_net_income(
        cls,
        owners_earnings: Union[int, float],
        net_income: Union[int, float],
    ) -> Union[int, float]:
        result = divide_or_zero(owners_earnings, net_income)
        return modify_for_percentage(result)
