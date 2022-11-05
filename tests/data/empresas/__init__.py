from bfet import DjangoTestingModel


from apps.empresas.models import (
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


def full_company():
    company = DjangoTestingModel.create(Company)
    DjangoTestingModel.create(IncomeStatement, company=company)
    DjangoTestingModel.create(BalanceSheet, company=company)
    DjangoTestingModel.create(CashflowStatement, company=company)
    return company


COMPANY_FINAL_STATEMENTS = full_company
