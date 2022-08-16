from typing import Type

from apps.empresas.models import Company
from apps.empresas.parse import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo
)
from apps.empresas.utils import log_company


class RetrieveCompanyData(FinnhubInfo, FinprepInfo, YahooQueryInfo, YFinanceInfo):
    def __init__(self, company: Type[Company]) -> None:
        super().__init__(company)
        self.company: Type[Company] = company

    @log_company("latest_financials_finprep_info")
    def create_financials_finprep(self):
        return super().create_financials_finprep()

    @log_company("first_financials_finnhub_info")
    def create_financials_finnhub(self):
        return super().create_financials_finnhub()

    @log_company("first_financials_yfinance_info")
    def create_financials_yfinance(self, period: str):
        if period == "q":
            return self.create_quarterly_financials_yfinance()
        return self.create_yearly_financials_yfinance()

    @log_company("first_financials_yahooquery_info")
    def create_financials_yahooquery(self, period: str):
        if period == "q":
            return self.create_quarterly_financials_yahooquery()
        return self.create_yearly_financials_yahooquery()

    @log_company("institutionals")
    def create_institutionals_yahooquery(self):
        return self.create_institutionals_yahooquery()
