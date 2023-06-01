from typing import Callable, Type

import pandas as pd

from src.empresas.models import (
    BalanceSheetYFinance,
    CashflowStatementYFinance,
    IncomeStatementYFinance,
)
from .normalize_data import NormalizeYFinance
from .parse_data import ParseYFinance
from src.general.outils.save_from_df import DFInfoCreator


class YFinanceInfo(DFInfoCreator, NormalizeYFinance, ParseYFinance):
    income_statement_model = IncomeStatementYFinance
    balance_sheet_model = BalanceSheetYFinance
    cashflow_statement_model = CashflowStatementYFinance

    def __init__(self, company) -> None:
        self.company = company
        self.normalize_income_statement = self.normalize_income_statements_yfinance
        self.normalize_balance_sheet = self.normalize_balance_sheets_yfinance
        self.normalize_cashflow_statement = self.normalize_cashflow_statements_yfinance

    def create_statements_from_df(
        self,
        df: Type[pd.DataFrame],
        period: Callable,
        function: Callable,
        model: Type,
    ):
        for column in df:
            model.objects.get_or_create(
                financials=df[column].to_dict(),
                defaults={**function(df[column], column, period)},
            )

    def create_quarterly_financials_yfinance(self):
        self.create_financials(
            self.request_quarterly_financials_yfinance,
            self.request_quarterly_balance_sheet_yfinance,
            self.request_quarterly_cashflow_yfinance,
            self.period_quarter,
        )

    def create_yearly_financials_yfinance(self):
        self.create_financials(
            self.request_financials_yfinance,
            self.request_balance_sheet_yfinance,
            self.request_cashflow_yfinance,
            self.period_year,
        )
