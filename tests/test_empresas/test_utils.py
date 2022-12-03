from datetime import datetime
from unittest import skip

from django.test import TestCase
from django.utils import timezone

from bfet import DjangoTestingModel

from src.empresas.utils import arrange_quarters, FinprepRequestCheck
from src.empresas.models import (
    Company,
    CompanyStockPrice,
    CompanyUpdateLog,
    CompanyYahooQueryProxy,
    CompanyYFinanceProxy,
    CompanyFinprepProxy,
    CompanyFinnhubProxy,
    CompanyStatementsProxy,
    Exchange,
    ExchangeOrganisation,
    BaseStatement,
    IncomeStatement,
    BalanceSheet,
    CashflowStatement,
    RentabilityRatio,
    LiquidityRatio,
    MarginRatio,
    FreeCashFlowRatio,
    PerShareValue,
    NonGaap,
    OperationRiskRatio,
    EnterpriseValueRatio,
    CompanyGrowth,
    EficiencyRatio,
    PriceToRatio,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
    BalanceSheetFinprep,
    CashflowStatementFinprep,
    IncomeStatementFinprep,
    BalanceSheetYFinance,
    CashflowStatementYFinance,
    IncomeStatementYFinance,
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
    IncomeStatementYahooQuery,
    KeyStatsYahooQuery,
    StatementsFinnhub,
)
from src.periods.models import Period


class TestUtils(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        cls.period = DjangoTestingModel.create(Period)
        cls.balancesheetyfinance = DjangoTestingModel.create(
            BalanceSheetYFinance,
            company=cls.company,
        )
        cls.cashflowstatementyfinance = DjangoTestingModel.create(
            CashflowStatementYFinance,
            company=cls.company,
        )
        cls.incomestatementyfinance = DjangoTestingModel.create(
            IncomeStatementYFinance,
            company=cls.company,
        )
        cls.balancesheetyahooquery = DjangoTestingModel.create(
            BalanceSheetYahooQuery,
            company=cls.company,
        )
        cls.cashflowstatementyahooquery = DjangoTestingModel.create(
            CashflowStatementYahooQuery,
            company=cls.company,
        )
        cls.incomestatementyahooquery = DjangoTestingModel.create(
            IncomeStatementYahooQuery,
            company=cls.company,
        )

    @skip("Not ready, will be improved")
    def test_arrange_quarters(self):
        arrange_quarters(self.company)


class TestFinprepRequestCheck(TestCase):
    def test_check_remaining_requests(self):
        yesterday = 1669368787
        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(120, yesterday, 30)
        assert is_auth is True
        assert 120 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(120, yesterday, 120)
        assert is_auth is True
        assert 120 == requests_done

        now = datetime.timestamp(timezone.now())
        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(120, now, 0)
        assert is_auth is True
        assert 120 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(3, now, 118)
        assert is_auth is False
        assert 121 == requests_done

        is_auth, last_request, requests_done = FinprepRequestCheck().check_remaining_requests(20, now, 40)
        assert is_auth is True
        assert 60 == requests_done

    @skip("need to find how to mock the file")
    def test_manage_track_requests(self):
        assert FinprepRequestCheck().manage_track_requests(120) is True
        assert FinprepRequestCheck().manage_track_requests(30) is False
