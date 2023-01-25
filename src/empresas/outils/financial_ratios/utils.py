from typing import Union

import yahooquery as yq
import yfinance as yf


def get_most_recent_price(ticker: str) -> float:
    yfinance_info = yf.Ticker(ticker).info
    current_price = yfinance_info.get("currentPrice")
    if not current_price:
        yahooquery_info = yq.Ticker(ticker).price
        for key in yahooquery_info.keys():
            current_price = yahooquery_info[key].get("regularMarketPrice", 0.0)
    return current_price


def calculate_compound_growth(
    numerator: Union[int, float],
    denominator: Union[int, float],
    years: int,
) -> Union[int, float]:
    return ((divide_or_zero(numerator, denominator) ** (1 / years)) - 1) * 100


def modify_for_percentage(value: Union[int, float], as_percentage: bool = True) -> Union[int, float]:
    return round(value * 100, 2) if as_percentage else value


def divide_or_zero(
    numerator: Union[int, float],
    denominator: Union[int, float],
    numbers_after_coma: int = 2,
) -> Union[int, float]:
    """A method to calculate a division that returns de product or 0 if the denominator is 0

    Parameters
    ----------
    numerator : Union[int, float]
        The numerator of the division
    denominator : Union[int, float]
        The denominator of the division
    numbers_after_coma: int
        The number of values after the coma

    Returns
    -------
    Union[int, float]
        The product of the division
    """
    try:
        return round(numerator / denominator, numbers_after_coma)
    except ZeroDivisionError:
        return 0
