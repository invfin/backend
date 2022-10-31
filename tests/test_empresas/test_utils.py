from unittest import skip

from django.test import TestCase

from bfet import DjangoTestingModel

from apps.empresas.utils import arrange_quarters
from apps.empresas.models import (
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
from apps.general.models import Period


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
