import math
from typing import Union

from src.empresas.outils.financial_ratios.utils import divide_or_zero, modify_for_percentage


def discounted_cashflow(
    last_revenue: Union[int, float],
    revenue_growth: Union[int, float],
    net_income_margin: Union[int, float],
    fcf_margin: Union[int, float],
    buyback: Union[int, float],
    average_shares_out: Union[int, float],
    required_return: Union[int, float] = 0.075,
    perpetual_growth: Union[int, float] = 0.025,
) -> Union[int, float]:
    today_value = fcf_expected = discount_factor = 0.0
    revenue_expected = last_revenue
    shares_outs = average_shares_out
    for i in range(1, 6):
        revenue_expected = revenue_expected * (1 + (revenue_growth / 100))
        income_expected = revenue_expected * (net_income_margin / 100)
        fcf_expected = income_expected * (fcf_margin / 100)
        discount_factor = (1 + required_return) ** i
        shares_outs = shares_outs * (1 - (buyback / 100))
        pv_future_cf = divide_or_zero(fcf_expected, discount_factor)
        today_value += pv_future_cf

    terminal_value = divide_or_zero(
        (fcf_expected * (1 + perpetual_growth)),
        (required_return - perpetual_growth),
    )
    pv_future_cf_tv = divide_or_zero(terminal_value, discount_factor)
    today_value += pv_future_cf_tv
    return round(divide_or_zero(today_value, shares_outs).real, 2)


def graham_value(
    current_eps: Union[int, float],
    book_per_share: Union[int, float],
) -> Union[int, float]:
    return round(math.sqrt(22.5 * max(current_eps, 0) * max(book_per_share, 0)), 2)


def margin_of_safety(
    value: Union[int, float],
    current_price: Union[int, float],
) -> Union[int, float]:
    return modify_for_percentage(1 - divide_or_zero(current_price, value))
