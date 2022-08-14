from typing import Type, Callable, Union

import pandas as pd

from apps.general.models import Period


class DFInfoCreator:
    period_quarter = Period.objects.first_quarter_period
    period_year = Period.objects.for_year_period
    income_statement_model = None
    balance_sheet_model = None
    cashflow_statement_model = None

    def __init__(self) -> None:
        self.normalize_income_statement = None
        self.normalize_balance_sheet = None
        self.normalize_cashflow_statement = None

    def create_statements_from_df(self):
        pass

    def create_statement(
        self,
        df: Type[pd.DataFrame],
        period: Callable,
        normalizer: Callable
    ):
        df = df.fillna(0)
        self.create_statements_from_df(df, period, normalizer, self.income_statement_model)

    def create_financials(
        self,
        incomes_df: Type[pd.DataFrame],
        balance_sheets_df: Type[pd.DataFrame],
        cashflows_df: Type[pd.DataFrame],
        period: Union[Period.objects.first_quarter_period, Period.objects.for_year_period]
    ):
        self.create_statement(
            incomes_df,
            period,
            self.normalize_income_statement
        )
        self.create_statement(
            balance_sheets_df,
            period,
            self.normalize_balance_sheet
        )
        self.create_statement(
            cashflows_df,
            period,
            self.normalize_cashflow_statement
        )
