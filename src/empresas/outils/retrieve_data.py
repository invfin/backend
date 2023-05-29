from datetime import datetime
from typing import Any, Dict, List, Type

from src.empresas.parse import FinnhubInfo, FinprepInfo, YahooQueryInfo, YFinanceInfo
from src.empresas.utils import log_company


class RetrieveCompanyData:
    def __init__(self, company: Type) -> None:
        self.company: Type = company

    def get_company_news(self) -> List:
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:]) - 2)
        from_date = datetime.now().strftime(f"%Y-%m-{day}")
        to_date = datetime.now().strftime("%Y-%m-%d")
        return FinnhubInfo(self.company).company_news(self.company.ticker, from_date, to_date)

    @log_company("latest_financials_finprep_info")
    def create_financials_finprep(self) -> Dict[str, Any]:
        return FinprepInfo(self.company).create_financials_finprep()

    @log_company("first_financials_finnhub_info")
    def create_financials_finnhub(self):
        return FinnhubInfo(self.company).create_financials_finnhub()

    @log_company("first_financials_yfinance_info")
    def create_financials_yfinance(self, period: str = "a"):
        if period == "q":
            return YFinanceInfo(self.company).create_quarterly_financials_yfinance()
        return YFinanceInfo(self.company).create_yearly_financials_yfinance()

    @log_company("first_financials_yahooquery_info")
    def create_financials_yahooquery(self, period: str = "a"):
        if period == "q":
            return YahooQueryInfo(self.company).create_quarterly_financials_yahooquery()
        return YahooQueryInfo(self.company).create_yearly_financials_yahooquery()

    @log_company("institutionals")
    def create_institutionals_yahooquery(self):
        return YahooQueryInfo(self.company).create_institutionals_yahooquery()

    @log_company("key_stats")
    def create_key_stats_yahooquery(self):
        return YahooQueryInfo(self.company).create_key_stats_yahooquery()
