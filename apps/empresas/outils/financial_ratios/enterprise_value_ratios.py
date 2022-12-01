from typing import Union


from .utils import divide_or_zero


class EnterpriseValueRatios:
    @classmethod
    def calculate_enterprise_value(
        cls,
        market_cap:Union[int, float],
        total_debt:Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return market_cap + total_debt - cash_and_short_term_investments

    @classmethod
    def calculate_ev_fcf(
        cls,
        algo:Union[int, float],
        algo:Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_ev_operating_cf(
        cls,
        algo:Union[int, float],
        algo:Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_ev_sales(
        cls,
        algo:Union[int, float],
        algo:Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_company_equity_multiplier(
        cls,
        current_price:Union[int, float],
        algo:Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_ev_multiple(
        cls,
        algo:Union[int, float],
        algo:Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero()

