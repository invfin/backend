from typing import List, Dict, Any

import yfinance as yf


class ParseYFinance:
    company = None

    @property
    def yfcompany(self):
        return yf.Ticker(self.company.ticker)

    @property
    def request_info_yfinance(self) -> Dict[str, Any]:
        # get stock info
        return self.yfcompany.info

    # get historical market data
    @property
    def request_history_yfinance(self):
        return self.yfcompany.history(period="max")

    # show actions (dividends, splits)
    @property
    def request_actions_yfinance(self):
        return self.yfcompany.actions

    # show dividends
    @property
    def request_dividends_yfinance(self):
        return self.yfcompany.dividends

    # show splits
    @property
    def request_splits_yfinance(self):
        return self.yfcompany.splits

    # show financials
    @property
    def request_financials_yfinance(self):
        return self.yfcompany.financials

    @property
    def request_quarterly_financials_yfinance(self):
        return self.yfcompany.quarterly_financials

    # show major holders
    @property
    def request_major_holders_yfinance(self):
        return self.yfcompany.major_holders

    # show institutional holders
    @property
    def request_institutional_holders_yfinance(self):
        return self.yfcompany.institutional_holders

    # show balance sheet
    @property
    def request_balance_sheet_yfinance(self):
        return self.yfcompany.balance_sheet

    @property
    def request_quarterly_balance_sheet_yfinance(self):
        return self.yfcompany.quarterly_balance_sheet

    # show cashflow
    @property
    def request_cashflow_yfinance(self):
        return self.yfcompany.cashflow

    @property
    def request_quarterly_cashflow_yfinance(self):
        return self.yfcompany.quarterly_cashflow

    # show earnings
    @property
    def request_earnings_yfinance(self):
        return self.yfcompany.earnings
    @property
    def request_quarterly_earnings_yfinance(self):
        return self.yfcompany.quarterly_earnings

    # show sustainability
    @property
    def request_sustainability_yfinance(self):
        return self.yfcompany.sustainability

    # show analysts recommendations
    @property
    def request_recommendations_yfinance(self):
        return self.yfcompany.recommendations

    # show next event (earnings, etc)
    @property
    def request_calendar_yfinance(self):
        return self.yfcompany.calendar

    # show all earnings dates
    @property
    def request_earnings_dates_yfinance(self):
        return self.yfcompany.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    @property
    def request_isin_yfinance(self):
        return self.yfcompany.isin

    # show options expirations
    @property
    def request_options_yfinance(self):
        return self.yfcompany.options

    # show news
    @property
    def request_news_yfinance(self):
        return self.yfcompany.news

    # get option chain for specific expiration
    # data available via: opt.calls, opt.puts
    @property
    def request_option_chain_yfinance(self):
        return self.yfcompany.option_chain('YYYY-MM-DD')


    @property
    def request_current_price_yfinance(self):
        return self.request_info_yfinance.get("currentPrice", 0)

    @property
    def request_currency_yfinance(self):
        return self.request_info_yfinance.get("currency", "Nan")
