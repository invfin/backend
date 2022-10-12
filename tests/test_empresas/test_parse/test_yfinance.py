import vcr
import pytest

from bfet import DjangoTestingModel as DTM
from apps.general.models import Period
from apps.empresas.models import Company
from apps.empresas.parse.y_finance import YFinanceInfo, NormalizeYFinance
from apps.empresas.models import BalanceSheetYFinance, CashflowStatementYFinance, IncomeStatementYFinance


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/yfinance/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


from django.test import TestCase


class TestYFinanceInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser = YFinanceInfo(cls.company)

    @parse_vcr.use_cassette
    def test_create_quarterly_financials_yfinance(self):
        period_2021 = Period.objects.first_quarter_period(2021)
        period_2022 = Period.objects.first_quarter_period(2022)
        assert 0 == BalanceSheetYFinance.objects.filter(period=period_2021).count()
        assert 0 == CashflowStatementYFinance.objects.filter(period=period_2021).count()
        assert 0 == IncomeStatementYFinance.objects.filter(period=period_2021).count()
        assert 0 == BalanceSheetYFinance.objects.filter(period=period_2022).count()
        assert 0 == CashflowStatementYFinance.objects.filter(period=period_2022).count()
        assert 0 == IncomeStatementYFinance.objects.filter(period=period_2022).count()
        self.parser.create_quarterly_financials_yfinance()
        assert 2 == BalanceSheetYFinance.objects.filter(period=period_2021).count()
        assert 2 == CashflowStatementYFinance.objects.filter(period=period_2021).count()
        assert 2 == IncomeStatementYFinance.objects.filter(period=period_2021).count()
        assert self.company == BalanceSheetYFinance.objects.filter(period=period_2021).first().company
        assert self.company == CashflowStatementYFinance.objects.filter(period=period_2021).first().company
        assert self.company == IncomeStatementYFinance.objects.filter(period=period_2021).first().company
        assert 2 == BalanceSheetYFinance.objects.filter(period=period_2022).count()
        assert 2 == CashflowStatementYFinance.objects.filter(period=period_2022).count()
        assert 2 == IncomeStatementYFinance.objects.filter(period=period_2022).count()
        assert self.company == BalanceSheetYFinance.objects.filter(period=period_2022).first().company
        assert self.company == CashflowStatementYFinance.objects.filter(period=period_2022).first().company
        assert self.company == IncomeStatementYFinance.objects.filter(period=period_2022).first().company

    @parse_vcr.use_cassette
    def test_create_yearly_financials_yfinance(self):
        assert 0 == BalanceSheetYFinance.objects.all().count()
        assert 0 == CashflowStatementYFinance.objects.all().count()
        assert 0 == IncomeStatementYFinance.objects.all().count()
        self.parser.create_yearly_financials_yfinance()
        for index in range(1, 4):
            year = 2018 + index
            period = Period.objects.for_year_period(year)
            with self.subTest(period):
                assert 1 == BalanceSheetYFinance.objects.filter(period=period).count()
                assert 1 == CashflowStatementYFinance.objects.filter(period=period).count()
                assert 1 == IncomeStatementYFinance.objects.filter(period=period).count()
