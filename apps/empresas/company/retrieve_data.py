from typing import Type

from apps.empresas.parse import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo
)
from apps.empresas.utils import log_company


class RetrieveCompanyData(FinnhubInfo, FinprepInfo, YahooQueryInfo, YFinanceInfo):
    def __init__(self, company: Type["Company"]) -> None:
        super().__init__(company)
        self.company: Type["Company"] = company



    @log_company
    def update_all_financials_from_yahoo(self):
        create_quarterly_financials_yfinance
        create_yearly_financials_yfinance
