from typing import List, Dict, Union, Any, Type
import requests
import time
import random

import yfinance as yf

from apps.general.outils.parser_client import ParserClient
from apps.empresas import constants
from apps.empresas.parse.y_finance.normalize_data import NormalizeYFinance


class ParseYFinance:
    def parse_single_company(self, ticker: str) -> yf.Ticker:
        return yf.Ticker(ticker)

    def parse_multiple_companies(self, tickers: List[str]) -> yf.Tickers:
        """
        yf.Tickers returns an object with symbols and tickers
        tickers -> Type[yf.Ticker]
        """
        return yf.Tickers(tickers)

    def company_info(self, company: Type[yf.Ticker]) -> Dict[str, Any]:
        # get stock info
        return company.info

    # get historical market data
    hist = msft.history(period="max")

    # show actions (dividends, splits)
    msft.actions

    # show dividends
    msft.dividends

    # show splits
    msft.splits

    # show financials
    msft.financials
    msft.quarterly_financials

    # show major holders
    msft.major_holders

    # show institutional holders
    msft.institutional_holders

    # show balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet

    # show cashflow
    msft.cashflow
    msft.quarterly_cashflow

    # show earnings
    msft.earnings
    msft.quarterly_earnings

    # show sustainability
    msft.sustainability

    # show analysts recommendations
    msft.recommendations

    # show next event (earnings, etc)
    msft.calendar

    # show all earnings dates
    msft.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    msft.isin

    # show options expirations
    msft.options

    # show news
    msft.news

    # get option chain for specific expiration
    opt = msft.option_chain('YYYY-MM-DD')

    # data available via: opt.calls, opt.puts

    def get_current_price(self):
        return yf.Ticker(self.ticker).info
        current_price = 0
        current_currency = 'None'

        try:
            company_info =
            if 'currentPrice' in company_info:
                current_price = company_info['currentPrice']
                current_currency = company_info['currency']
            else:
                company_info = yq.Ticker(self.ticker).financial_data
                if 'currentPrice' in company_info:
                    current_price = company_info['currentPrice']
                    current_currency = company_info['financialCurrency']

        except Exception as e:
            current_price, current_currency = self.scrap_price_yahoo()

        return {
            'current_price': current_price,
            'current_currency': current_currency,
        }
