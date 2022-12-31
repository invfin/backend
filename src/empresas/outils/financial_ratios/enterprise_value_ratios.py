from typing import Union

from .utils import divide_or_zero


class EnterpriseValueRatios:
    @classmethod
    def calculate_enterprise_value(
        cls,
        market_cap: Union[int, float],
        total_debt: Union[int, float],
        cash_and_short_term_investments: Union[int, float],
    ) -> Union[int, float]:
        return market_cap + total_debt - cash_and_short_term_investments

    @classmethod
    def calculate_ev_fcf(
        cls,
        enterprise_value: Union[int, float],
        free_cash_flow: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(enterprise_value, free_cash_flow)

    @classmethod
    def calculate_ev_operating_cf(
        cls,
        enterprise_value: Union[int, float],
        net_cash_provided_by_operating_activities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(enterprise_value, net_cash_provided_by_operating_activities)

    @classmethod
    def calculate_ev_sales(
        cls,
        enterprise_value: Union[int, float],
        revenue: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(enterprise_value, revenue)

    @classmethod
    def calculate_company_equity_multiplier(
        cls,
        total_assets: Union[int, float],
        total_stockholders_equity: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_assets, total_stockholders_equity)

    @classmethod
    def calculate_ev_multiple(
        cls,
        enterprise_value: Union[int, float],
        ebitda: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(enterprise_value, ebitda)
