from typing import Type, Callable
from datetime import datetime

import pandas as pd

from apps.general import constants
from apps.general.outils.save_from_df import DFInfoCreator
from apps.general.models import Period
from apps.empresas.models import (
    BalanceSheetYahooQuery,
    IncomeStatementYahooQuery,
    CashflowStatementYahooQuery,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
    KeyStatsYahooQuery
)
from apps.empresas.parse.yahoo_query.normalize_data import NormalizeYahooQuery
from apps.empresas.parse.yahoo_query.parse_data import ParseYahooQuery



class YahooQueryInfo(DFInfoCreator, NormalizeYahooQuery, ParseYahooQuery):
    income_statement_model = IncomeStatementYahooQuery
    balance_sheet_model = BalanceSheetYahooQuery
    cashflow_statement_model = CashflowStatementYahooQuery

    def __init__(self, company) -> None:
        self.company = company
        self.normalize_income_statement = self.normalize_income_statements_yahooquery
        self.normalize_balance_sheet = self.normalize_balance_sheets_yahooquery
        self.normalize_cashflow_statement = self.normalize_cashflow_statements_yahooquery

    def match_quarters_with_earning_history_yahooquery(self):
        df = self.request_earning_history_yahooquery
        quarter_matching = {
            "-1q": constants.PERIOD_3_QUARTER,
            "-2q": constants.PERIOD_2_QUARTER,
            "-3q": constants.PERIOD_1_QUARTER,
            "-4q": constants.PERIOD_4_QUARTER,
        }
        prev_period = None
        for index, data in df.iterrows():
            quarter = data.get("period")
            year = data.get("quarter")
            year_date_obj = datetime.strptime(year, '%Y-%m-%d').date()
            actual_quarter = quarter_matching[quarter]
            actual_year = year_date_obj.year
            if prev_period:
                if prev_period.period == constants.PERIOD_4_QUARTER:
                    actual_year = year_date_obj.year + 1

            actual_period, created = Period.objects.get_or_create(year=actual_year, period=actual_quarter)
            prev_period = actual_period
            self.company.incomestatementyahooquery_set.filter(
                year=year_date_obj
            ).exclude(
                period__period=constants.PERIOD_FOR_YEAR
            ).update(period=actual_period)
            self.company.balancesheetyahooquery_set.filter(
                year=year_date_obj
            ).exclude(
                period__period=constants.PERIOD_FOR_YEAR
            ).update(period=actual_period)
            self.company.cashflowstatementyahooquery_set.filter(
                year=year_date_obj
            ).exclude(
                period__period=constants.PERIOD_FOR_YEAR
            ).update(period=actual_period)

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
            # if model.objects.filter(
            #     as_of_date=financials_data["asOfDate"],
            #     period_type=financials_data["periodType"]
            # ).exists():
            #     print("existo")
            # else:
            #     print("no existo")
            #     print(model.objects.filter(
            #         as_of_date=financials_data["asOfDate"],
            #         period_type=financials_data["periodType"]
            #     ))
            #     continue
            model.objects.create(
                financials=financials_data,
                **function(data, period)
            )
            # print(m)
            print("*"*100)

    def create_quarterly_financials_yahooquery(self):
        self.create_financials(
            self.request_income_statements_yahooquery("q"),
            self.request_balance_sheets_yahooquery("q"),
            self.request_cashflow_statements_yahooquery("q"),
            self.period_quarter
        )

    def create_yearly_financials_yahooquery(self):
        self.create_financials(
            self.request_income_statements_yahooquery(),
            self.request_balance_sheets_yahooquery(),
            self.request_cashflow_statements_yahooquery(),
            self.period_year
        )

    def create_institutionals_yahooquery(self):
        df_institution_ownership = self.yqcompany.institution_ownership
        df = self.normalize_institutional_yahooquery(df_institution_ownership)
        for index, data in df.iterrows():
            institution, created = InstitutionalOrganization.objects.get_or_create(
                name=data['organization']
            )
            if TopInstitutionalOwnership.objects.filter(
                year=data['reportDate'],
                company=self.company,
                organization=institution,
            ).exists():
                continue
            TopInstitutionalOwnership.objects.create(
                date=data['reportDate'][:4],
                year=data['reportDate'],
                company=self.company,
                organization=institution,
                percentage_held=data['pctHeld'],
                position=data['position'],
                value=data['value']
            )

    def create_key_stats_yahooquery(self):
        key_stats = self.request_key_stats_yahooquery
        for key in key_stats.keys():
            KeyStatsYahooQuery.objects.get_or_create(
                **self.normalize_key_stats_yahooquery(key_stats[key])
            )
