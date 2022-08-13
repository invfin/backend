from typing import List, Dict, Union, Any, Type

import yfinance as yf


class ParseYFinance:
    def __init__(self, ticker) -> None:
        self.company = yf.Ticker(ticker)

    def parse_multiple_companies_yfinance(self, tickers: List[str]) -> yf.Tickers:
        """
        yf.Tickers returns an object with symbols and tickers
        tickers -> Type[yf.Ticker]
        """
        return yf.Tickers(tickers)

    @property
    def request_company_info_yfinance(self) -> Dict[str, Any]:
        # get stock info
        return self.company.info

    # get historical market data
    @property
    def request_company_history_yfinance(self):
        return self.company.history(period="max")

    # show actions (dividends, splits)
    @property
    def request_company_actions_yfinance(self):
        return self.company.actions

    # show dividends
    @property
    def request_company_dividends_yfinance(self):
        return self.company.dividends

    # show splits
    @property
    def request_company_splits_yfinance(self):
        return self.company.splits

    # show financials
    @property
    def request_company_financials_yfinance(self):
        return self.company.financials

    @property
    def request_company_quarterly_financials_yfinance(self):
        return self.company.quarterly_financials

    # show major holders
    @property
    def request_company_major_holders_yfinance(self):
        return self.company.major_holders

    # show institutional holders
    @property
    def request_company_institutional_holders_yfinance(self):
        return self.company.institutional_holders

    # show balance sheet
    @property
    def request_company_balance_sheet_yfinance(self):
        return self.company.balance_sheet

    @property
    def request_company_quarterly_balance_sheet_yfinance(self):
        return self.company.quarterly_balance_sheet

    # show cashflow
    @property
    def request_company_cashflow_yfinance(self):
        return self.company.cashflow

    @property
    def request_company_quarterly_cashflow_yfinance(self):
        return self.company.quarterly_cashflow

    # show earnings
    @property
    def request_company_earnings_yfinance(self):
        return self.company.earnings
    @property
    def request_company_quarterly_earnings_yfinance(self):
        return self.company.quarterly_earnings

    # show sustainability
    @property
    def request_company_sustainability_yfinance(self):
        return self.company.sustainability

    # show analysts recommendations
    @property
    def request_company_recommendations_yfinance(self):
        return self.company.recommendations

    # show next event (earnings, etc)
    @property
    def request_company_calendar_yfinance(self):
        return self.company.calendar

    # show all earnings dates
    @property
    def request_company_earnings_dates_yfinance(self):
        return self.company.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    @property
    def request_company_isin_yfinance(self):
        return self.company.isin

    # show options expirations
    @property
    def request_company_options_yfinance(self):
        return self.company.options

    # show news
    @property
    def request_company_news_yfinance(self):
        return self.company.news

    # get option chain for specific expiration
    # data available via: opt.calls, opt.puts
    @property
    def request_company_option_chain_yfinance(self):
        return self.company.option_chain('YYYY-MM-DD')


    @property
    def request_company_current_price_yfinance(self):
        return self.request_company_info_yfinance.get("currentPrice", 0)

    @property
    def request_company_currency_yfinance(self):
        return self.request_company_info_yfinance.get("currency", "Nan")
