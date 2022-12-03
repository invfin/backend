from typing import Dict, List
from bfet import DjangoTestingModel

from django.utils import timezone

from src.empresas.models import (
    CompanyYahooQueryProxy,
    CompanyYFinanceProxy,
    CompanyFinprepProxy,
    CompanyFinnhubProxy,
    CompanyStatementsProxy,
    Company,
    CompanyStockPrice,
    CompanyUpdateLog,
    Exchange,
    ExchangeOrganisation,
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
from src.industries_sectors.models import (
    Industry,
    Sector,
)
from src.periods.models import Period
from src.periods import constants


class CreateExchanges:
    def create_sectors():
        sector = DjangoTestingModel.create(Sector)
        industry = DjangoTestingModel.create(Industry)
        exchange_org_fr = DjangoTestingModel.create(ExchangeOrganisation, name="France")
        exchange_org_usa = DjangoTestingModel.create(ExchangeOrganisation, name="Estados Unidos")
        exchange_nyse = DjangoTestingModel.create(Exchange, exchange_ticker="NYSE", main_org=exchange_org_usa)
        exchange_euro = DjangoTestingModel.create(Exchange, exchange_ticker="EURO", main_org=exchange_org_fr)


class CreateCompany:
    def create_company(self):
        apple = DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=True,
            updated=False,
            has_error=True,
            exchange=cls.exchange_nyse,
            checkings={"has_institutionals": {"state": "no", "time": ""}},
        )


class CreateStatements:
    periods: Dict[int, List[Period]] = {
        constants.PERIOD_1_QUARTER: [],
        constants.PERIOD_2_QUARTER: [],
        constants.PERIOD_3_QUARTER: [],
        constants.PERIOD_4_QUARTER: [],
        constants.PERIOD_FOR_YEAR: [],
    }
    statements: Dict[int, List[Period]] = {
        constants.PERIOD_1_QUARTER: [],
        constants.PERIOD_2_QUARTER: [],
        constants.PERIOD_3_QUARTER: [],
        constants.PERIOD_4_QUARTER: [],
        constants.PERIOD_FOR_YEAR: [],
    }
    company: Company = None

    def create_statement(self, company, period) -> IncomeStatement:
        return DjangoTestingModel.create(IncomeStatement, company=company, period=period)

    def create_period(self, year, period):
        return DjangoTestingModel.create(Period, year=year, period=period)

    def create_data(self, use_company: bool = True):
        if use_company:
            company = DjangoTestingModel.create(Company)
            self.company = company
        current_year = timezone.now().year
        for period_time in constants.PERIODS:
            for index in range(3):
                past_year = current_year - index
                next_year = current_year + index
                period_object_past_year = self.create_period(year=past_year, period=period_time)
                period_object_next_year = self.create_period(year=next_year, period=period_time)
                statement_past_year = self.create_statement(company, period_object_past_year)
                statement_next_year = self.create_statement(company, period_object_next_year)
                self.periods[period_time].append(period_object_past_year, period_object_next_year)
                self.statements[period_time].append(statement_past_year, statement_next_year)
