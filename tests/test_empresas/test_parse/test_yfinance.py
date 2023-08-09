from unittest import skip

from django.test import TestCase

from bfet import DjangoTestingModel
import vcr

from src.empresas.models import (
    BalanceSheetYFinance,
    CashflowStatementYFinance,
    Company,
    IncomeStatementYFinance,
)
from src.empresas.information_sources.y_finance import YFinanceInfo
from src.periods.models import Period

parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/yfinance/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("currently yfinacne seems to be failing")
class TestYFinanceInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DjangoTestingModel.create(Company, ticker="AAPL")
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
        assert (
            self.company
            == BalanceSheetYFinance.objects.filter(period=period_2021).first().company
        )
        assert (
            self.company
            == CashflowStatementYFinance.objects.filter(period=period_2021).first().company
        )
        assert (
            self.company
            == IncomeStatementYFinance.objects.filter(period=period_2021).first().company
        )
        assert 2 == BalanceSheetYFinance.objects.filter(period=period_2022).count()
        assert 2 == CashflowStatementYFinance.objects.filter(period=period_2022).count()
        assert 2 == IncomeStatementYFinance.objects.filter(period=period_2022).count()
        assert (
            self.company
            == BalanceSheetYFinance.objects.filter(period=period_2022).first().company
        )
        assert (
            self.company
            == CashflowStatementYFinance.objects.filter(period=period_2022).first().company
        )
        assert (
            self.company
            == IncomeStatementYFinance.objects.filter(period=period_2022).first().company
        )

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
