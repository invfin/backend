from typing import Union

import yfinance as yf
import yahooquery as yq


def get_most_recent_price(ticker: str) -> float:
    yfinance_info = yf.Ticker(ticker).info
    current_price = yfinance_info.get("currentPrice")
    if not current_price:
        yahooquery_info = yq.Ticker(ticker).price
        for key in yahooquery_info.keys():
            current_price = yahooquery_info[key].get("regularMarketPrice", 0.0)
    return current_price


def divide_or_zero(numerator: Union[int, float], denominator: Union[int, float]):
    """A method to calculate a divison that returns de product or 0 if the denominator is 0

    Parameters
    ----------
    numerator : Union[int, float]
        The numerator of the division
    denominator : Union[int, float]
        The denominator of the division

    Returns
    -------
    Union[int, float]
        The product of the division
    """
    return round(numerator / denominator, 2) if denominator != 0 else 0
