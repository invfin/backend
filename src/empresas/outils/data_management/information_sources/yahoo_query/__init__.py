from typing import Callable, Type

import pandas as pd

from src.empresas.models import (
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
    IncomeStatementYahooQuery,
    InstitutionalOrganization,
    KeyStatsYahooQuery,
    TopInstitutionalOwnership,
)
from src.empresas.information_sources.yahoo_query.normalize_data import NormalizeYahooQuery
from src.empresas.information_sources.yahoo_query.parse_data import ParseYahooQuery
from src.general.outils.save_from_df import DFInfoCreator


class YahooQueryInfo(DFInfoCreator):
    income_statement_model = IncomeStatementYahooQuery
    balance_sheet_model = BalanceSheetYahooQuery
    cashflow_statement_model = CashflowStatementYahooQuery

    def __init__(self, company) -> None:
        self.company = company
        self.yahooquery = ParseYahooQuery(company.ticker)
        self.normalize_income_statement = (
            NormalizeYahooQuery.normalize_income_statements_yahooquery
        )
        self.normalize_balance_sheet = NormalizeYahooQuery.normalize_balance_sheets_yahooquery
        self.normalize_cashflow_statement = (
            NormalizeYahooQuery.normalize_cashflow_statements_yahooquery
        )

    def create_statements_from_df(
        self,
        df: pd.DataFrame,
        period: Callable,
        normalizer: Callable,
        model: Type,
    ):
        """
        This method is called by create_financials.
        It belongs to DFInfoCreator and in each class it's overriden to be
        adapted to each dataframe.
        """
        for index, data in df.iterrows():
            financials_data = data.to_dict()
            financials_data["asOfDate"] = (
                financials_data["asOfDate"].to_pydatetime().date().strftime("%m/%d/%Y")
            )
            model.objects.get_or_create(
                financials=financials_data, defaults=normalizer(data, period, self.company)
            )

    def create_quarterly_financials_yahooquery(self):
        self.create_financials(
            self.yahooquery.request_income_statements_yahooquery("q"),
            self.yahooquery.request_balance_sheets_yahooquery("q"),
            self.yahooquery.request_cashflow_statements_yahooquery("q"),
            self.period_quarter,
        )

    def create_yearly_financials_yahooquery(self):
        self.create_financials(
            self.yahooquery.request_income_statements_yahooquery(),
            self.yahooquery.request_balance_sheets_yahooquery(),
            self.yahooquery.request_cashflow_statements_yahooquery(),
            self.period_year,
        )

    def create_institutionals_yahooquery(self):
        df_institution_ownership = self.yahooquery.yqcompany.institution_ownership
        df = NormalizeYahooQuery.normalize_institutional_yahooquery(df_institution_ownership)
        for index, data in df.iterrows():
            institution, created = InstitutionalOrganization.objects.get_or_create(
                name=data["organization"]
            )
            if TopInstitutionalOwnership.objects.filter(
                year=data["reportDate"],
                company=self.company,
                organization=institution,
            ).exists():
                continue
            TopInstitutionalOwnership.objects.create(
                date=data["reportDate"][:4],
                year=data["reportDate"],
                company=self.company,
                organization=institution,
                percentage_held=data["pctHeld"],
                position=data["position"],
                value=data["value"],
            )

    def create_key_stats_yahooquery(self):
        for value in self.yahooquery.request_key_stats_yahooquery.values():
            KeyStatsYahooQuery.objects.get_or_create(
                **NormalizeYahooQuery.normalize_key_stats_yahooquery(value, self.company)
            )
