from typing import Type

from apps.empresas.parse import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo
)


class RetrieveCompanyData(FinnhubInfo, FinprepInfo, YahooQueryInfo, YFinanceInfo):
    def __init__(self, company: Type["Company"]) -> None:
        super().__init__()
        self.company: Type["Company"] = company
