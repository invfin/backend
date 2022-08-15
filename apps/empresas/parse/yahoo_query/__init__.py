from typing import Type, Callable
import pandas as pd

from apps.empresas.models import BalanceSheetYahooQuery, IncomeStatementYahooQuery, CashflowStatementYahooQuery
from apps.empresas.parse.yahoo_query.normalize_data import NormalizeYahooQuery
from apps.empresas.parse.yahoo_query.parse_data import ParseYahooQuery
from apps.general.outils.save_from_df import DFInfoCreator


class YahooQueryInfo(DFInfoCreator, NormalizeYahooQuery, ParseYahooQuery):
    income_statement_model = IncomeStatementYahooQuery
    balance_sheet_model = BalanceSheetYahooQuery
    cashflow_statement_model = CashflowStatementYahooQuery

    def __init__(self, company) -> None:
        self.company = company
        self.normalize_income_statement = self.normalize_income_statements_yahooquery
        self.normalize_balance_sheet = self.normalize_balance_sheets_yahooquery
        self.normalize_cashflow_statement = self.normalize_cashflow_statements_yahooquery

    def create_statements_from_df(
        self,
        df: Type[pd.DataFrame],
        period: Callable,
        function: Callable,
        model: Type
    ):
        """
        param: function is the normalizer to regularise the data to be saved
        param: model is the model where the data is saved
        """
        for index, data in df.iterrows():
            financials_data = data.to_dict()
            financials_data["asOfDate"] = financials_data["asOfDate"].to_pydatetime().date().strftime("%m/%d/%Y")
            model.objects.create(
                financials=financials_data,
                **self.initial_data(data["asOfDate"], period, data["currencyCode"])
                # **function(data, period)
            )
        return

    def create_quarterly_financials_yfinance(self):
        self.create_financials(
            self.request_income_statements_yahooquery("q"),
            self.request_balance_sheets_yahooquery("q"),
            self.request_cashflow_statements_yahooquery("q"),
            self.period_quarter
        )

    def create_yearly_financials_yfinance(self):
        self.create_financials(
            self.request_income_statements_yahooquery(),
            self.request_balance_sheets_yahooquery(),
            self.request_cashflow_statements_yahooquery(),
            self.period_year
        )
