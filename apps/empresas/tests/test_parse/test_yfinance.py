import vcr

from django.test import TestCase

from apps.bfet import ExampleModel
from apps.general.models import Period
from apps.empresas.models import Company
from apps.empresas.parse.y_finance import YFinanceInfo, NormalizeYFinance
from apps.empresas.models import BalanceSheetYFinance, CashflowStatementYFinance, IncomeStatementYFinance


parse_vcr = vcr.VCR(
    cassette_library_dir='cassettes/company/parse/yfinance/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestYFinanceInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = ExampleModel.create(Company, ticker="AAPL")
        cls.parser = YFinanceInfo(cls.company)

    @parse_vcr.use_cassette
    def test_create_quarterly_financials_yfinance(self):
        BalanceSheetYFinance.objects.filter().count()
        CashflowStatementYFinance.objects.filter().count()
        IncomeStatementYFinance.objects.filter().count()
        self.parser.create_quarterly_financials_yfinance()

    @parse_vcr.use_cassette
    def test_create_yearly_financials_yfinance(self):
        BalanceSheetYFinance.objects.filter().count()
        CashflowStatementYFinance.objects.filter().count()
        IncomeStatementYFinance.objects.filter().count()
        self.parser.create_yearly_financials_yfinance()

class TestNormalizeYFinance(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.normalizer = NormalizeYFinance()
