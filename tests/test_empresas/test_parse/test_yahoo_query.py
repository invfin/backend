from datetime import datetime
from unittest import skip
from unittest.mock import patch

from django.test import TestCase

from bfet import DjangoTestingModel

from tests.data.empresas.yahooquery import list_to_dataframe

from src.empresas.models import (
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
    Company,
    IncomeStatementYahooQuery,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
)
from src.empresas.parse.yahoo_query import YahooQueryInfo
from src.periods.models import Period


# TODO patch the requests and responses
@skip("needs to be patched")
class TestYahooQueryInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DjangoTestingModel.create(Company, ticker="AAPL")
        cls.parser = YahooQueryInfo(cls.company)
        cls.current_year = datetime.now().year

    @patch("src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_income_statements_yahooquery")
    @patch("src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_income_statements_yahooquery")
    @patch("src.empresas.parse.yahoo_query.parse_data.ParseYahooQuery.request_income_statements_yahooquery")
    def test_create_quarterly_financials_yahooquery(self, mock_inc, mock_bs, mock_cf):
        mock_inc.return_value = list_to_dataframe()
        mock_bs.return_value = list_to_dataframe()
        mock_cf.return_value = list_to_dataframe()
        period_2021 = Period.objects.first_quarter_period(self.current_year - 1)
        period_2022 = Period.objects.first_quarter_period(self.current_year)
        assert 0 == BalanceSheetYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == CashflowStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == IncomeStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == BalanceSheetYahooQuery.objects.filter(period=period_2022).count()
        assert 0 == CashflowStatementYahooQuery.objects.filter(period=period_2022).count()
        assert 0 == IncomeStatementYahooQuery.objects.filter(period=period_2022).count()
        self.parser.create_quarterly_financials_yahooquery()
        assert 2 == BalanceSheetYahooQuery.objects.filter(period=period_2021).count()
        assert 2 == CashflowStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 2 == IncomeStatementYahooQuery.objects.filter(period=period_2021).count()
        assert self.company == BalanceSheetYahooQuery.objects.filter(period=period_2021).first().company
        assert self.company == CashflowStatementYahooQuery.objects.filter(period=period_2021).first().company
        assert self.company == IncomeStatementYahooQuery.objects.filter(period=period_2021).first().company
        assert 2 == BalanceSheetYahooQuery.objects.filter(period=period_2022).count()
        assert 2 == CashflowStatementYahooQuery.objects.filter(period=period_2022).count()
        assert 2 == IncomeStatementYahooQuery.objects.filter(period=period_2022).count()
        assert self.company == BalanceSheetYahooQuery.objects.filter(period=period_2022).first().company
        assert self.company == CashflowStatementYahooQuery.objects.filter(period=period_2022).first().company
        assert self.company == IncomeStatementYahooQuery.objects.filter(period=period_2022).first().company

    @skip("needs to be patched")
    def test_create_yearly_financials_yahooquery(self):
        assert 0 == BalanceSheetYahooQuery.objects.all().count()
        assert 0 == CashflowStatementYahooQuery.objects.all().count()
        assert 0 == IncomeStatementYahooQuery.objects.all().count()
        self.parser.create_yearly_financials_yahooquery()
        for index in range(1, 4):
            year = (self.current_year - 4) + index
            period = Period.objects.for_year_period(year)
            with self.subTest(period):
                assert 1 == BalanceSheetYahooQuery.objects.filter(period=period).count()
                assert 1 == CashflowStatementYahooQuery.objects.filter(period=period).count()
                assert 1 == IncomeStatementYahooQuery.objects.filter(period=period).count()

    @skip("method needs improvement")
    def test_create_institutionals_yahooquery(self):
        assert 0 == InstitutionalOrganization.objects.all().count()
        assert 0 == TopInstitutionalOwnership.objects.all().count()
        self.parser.normalize_institutional_yahooquery()
