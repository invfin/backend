import vcr
import pytest

from unittest import skip
from datetime import datetime

from bfet import DjangoTestingModel as DTM
from apps.general.models import Period
from apps.empresas.models import (
    Company,
    BalanceSheetYahooQuery,
    IncomeStatementYahooQuery,
    CashflowStatementYahooQuery,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
)
from apps.empresas.parse.yahoo_query import ParseYahooQuery, YahooQueryInfo


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/yahoo_query",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


from django.test import TestCase


class TestYahooQueryInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser = YahooQueryInfo(cls.company)
        cls.current_year = datetime.now().year

    def test_create_quarterly_financials_yfinance(self):
        period_2021 = Period.objects.first_quarter_period(self.current_year - 1)
        period_2022 = Period.objects.first_quarter_period(self.current_year)
        assert 0 == BalanceSheetYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == CashflowStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == IncomeStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 0 == BalanceSheetYahooQuery.objects.filter(period=period_2022).count()
        assert 0 == CashflowStatementYahooQuery.objects.filter(period=period_2022).count()
        assert 0 == IncomeStatementYahooQuery.objects.filter(period=period_2022).count()
        self.parser.create_quarterly_financials_yfinance()
        assert 3 == BalanceSheetYahooQuery.objects.filter(period=period_2021).count()
        assert 3 == CashflowStatementYahooQuery.objects.filter(period=period_2021).count()
        assert 3 == IncomeStatementYahooQuery.objects.filter(period=period_2021).count()
        assert self.company == BalanceSheetYahooQuery.objects.filter(period=period_2021).first().company
        assert self.company == CashflowStatementYahooQuery.objects.filter(period=period_2021).first().company
        assert self.company == IncomeStatementYahooQuery.objects.filter(period=period_2021).first().company
        assert 2 == BalanceSheetYahooQuery.objects.filter(period=period_2022).count()
        assert 2 == CashflowStatementYahooQuery.objects.filter(period=period_2022).count()
        assert 2 == IncomeStatementYahooQuery.objects.filter(period=period_2022).count()
        assert self.company == BalanceSheetYahooQuery.objects.filter(period=period_2022).first().company
        assert self.company == CashflowStatementYahooQuery.objects.filter(period=period_2022).first().company
        assert self.company == IncomeStatementYahooQuery.objects.filter(period=period_2022).first().company

    def test_create_yearly_financials_yfinance(self):
        assert 0 == BalanceSheetYahooQuery.objects.all().count()
        assert 0 == CashflowStatementYahooQuery.objects.all().count()
        assert 0 == IncomeStatementYahooQuery.objects.all().count()
        self.parser.create_yearly_financials_yfinance()
        for index in range(1, 4):
            year = (self.current_year - 4) + index
            period = Period.objects.for_year_period(year)
            with self.subTest(period):
                assert 1 == BalanceSheetYahooQuery.objects.filter(period=period).count()
                assert 1 == CashflowStatementYahooQuery.objects.filter(period=period).count()
                assert 1 == IncomeStatementYahooQuery.objects.filter(period=period).count()

    def test_create_institutionals_yahooquery(self):
        assert 0 == InstitutionalOrganization.objects.all().count()
        assert 0 == TopInstitutionalOwnership.objects.all().count()
        self.parser.normalize_institutional_yahooquery()
