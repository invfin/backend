from typing import Type

from apps.empresas.parse import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo
)
from apps.empresas.utils import log_company


class RetrieveCompanyData:
    def __init__(self, company: Type["Company"]) -> None:
        self.company: Type["Company"] = company
        self.finprep = FinprepInfo(company)
        self.finnhub = FinnhubInfo(company)
        self.yahooquery = YahooQueryInfo(company)
        self.yfinance = YFinanceInfo(company)

    def get_most_recent_price(self):
        yfinance_info = self.yfinance.request_info_yfinance
        if 'currentPrice' in yfinance_info:
            current_price = yfinance_info['currentPrice']
        else:
            yahooquery_info = self.yahooquery.request_price_info_yahooquery
            for key in yahooquery_info.keys():
                current_price = yahooquery_info[key]['regularMarketPrice']
        return {'currentPrice': current_price}

    @log_company("latest_financials_finprep_info")
    def create_financials_finprep(self):
        return self.finprep.create_financials_finprep()

    @log_company("first_financials_finnhub_info")
    def create_financials_finnhub(self):
        return self.finnhub.create_financials_finnhub()

    @log_company("first_financials_yfinance_info")
    def create_financials_yfinance(self, period: str):
        if period == "q":
            return self.yfinance.create_quarterly_financials_yfinance()
        return self.yfinance.create_yearly_financials_yfinance()

    @log_company("first_financials_yahooquery_info")
    def create_financials_yahooquery(self, period: str):
        if period == "q":
            return self.yahooquery.create_quarterly_financials_yahooquery()
        return self.yahooquery.create_yearly_financials_yahooquery()

    @log_company("institutionals")
    def create_institutionals_yahooquery(self):
        return self.yahooquery.create_institutionals_yahooquery()

    @log_company("key_stats")
    def create_key_stats_yahooquery(self):
        return self.yahooquery.create_key_stats_yahooquery()
