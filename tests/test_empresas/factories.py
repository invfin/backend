from bfet import DjangoTestingModel as DTM, DataCreator

from apps.general.constants import PERIOD_FOR_YEAR
from apps.general.models import Country, Period, Sector, Currency
from apps.general.tests.data import SECTORS, COUNTRIES
from apps.empresas.outils.update import UpdateCompany
from apps.socialmedias.test_socialmedias.data import AAPL
from apps.empresas.tests.finprep_data import INCOME_STATEMENT, BALANCE_SHEET, CASHFLOW_STATEMENT
from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    IncomeStatementYFinance,
    IncomeStatementFinprep,
    BalanceSheetYahooQuery,
    BalanceSheetYFinance,
    BalanceSheetFinprep,
    CashflowStatementYahooQuery,
    CashflowStatementYFinance,
    CashflowStatementFinprep,
)


class AppleExample:
    def create_company(self):
        Country.objects.get_or_create(**COUNTRIES[0])
        Sector.objects.get_or_create(**SECTORS[0])
        company = Company.objects.create(**AAPL)
        return company

    def include_fianancials(self):
        company = self.create_company()
        update_company = UpdateCompany(company)
        for inc in INCOME_STATEMENT:
            update_company.create_income_statement(inc)
        for bs in BALANCE_SHEET:
            update_company.create_balance_sheet(bs)
        for cf in CASHFLOW_STATEMENT:
            update_company.create_cashflow_statement(cf)
        update_company.create_all_ratios(
            update_company.calculate_all_ratios(INCOME_STATEMENT, BALANCE_SHEET, CASHFLOW_STATEMENT)
        )
        return company

    @classmethod
    def return_example(cls):
        return cls().include_fianancials()


class CompanyExample:
    @classmethod
    def create_example_company(cls):
        cls.company = DTM.create(Company)
        cls.period = DTM.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.currency = DTM.create(Currency)
        cls.revenue = DataCreator.create_random_float()
        cls.cost_of_revenue = DataCreator.create_random_float()
        cls.gross_profit = DataCreator.create_random_float()
        cls.research_and_development_expenses = DataCreator.create_random_float()
        cls.selling_general_and_administrative_expenses = DataCreator.create_random_float()
        cls.inc_st_finprep = DTM.create(
            IncomeStatementFinprep,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            revenue=cls.revenue,
            cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_and_development_expenses=cls.research_and_development_expenses,
            selling_general_and_administrative_expenses=cls.selling_general_and_administrative_expenses,
        )
        cls.inc_st_yahooquery = DTM.create(
            IncomeStatementYahooQuery,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            total_revenue=cls.revenue,
            reconciled_cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_and_development=cls.research_and_development_expenses,
            selling_general_and_administration=cls.selling_general_and_administrative_expenses,
        )
        cls.inc_st_yfinance = DTM.create(
            IncomeStatementYFinance,
            reported_currency=cls.currency,
            company=cls.company,
            period=cls.period,
            total_revenue=cls.revenue,
            cost_of_revenue=cls.cost_of_revenue,
            gross_profit=cls.gross_profit,
            research_development=cls.research_and_development_expenses,
            selling_general_administrative=cls.selling_general_and_administrative_expenses,
        )
        cls.bs_finprep = DTM.create(BalanceSheetFinprep, company=cls.company, period=cls.period)
        cls.bs_yahooquery = DTM.create(BalanceSheetYahooQuery, company=cls.company, period=cls.period)
        cls.bs_yfinance = DTM.create(BalanceSheetYFinance, company=cls.company, period=cls.period)
        cls.cf_st_finprep = DTM.create(CashflowStatementFinprep, company=cls.company, period=cls.period)
        cls.cf_st_yahooquery = DTM.create(CashflowStatementYahooQuery, company=cls.company, period=cls.period)
        cls.cf_st_yfinance = DTM.create(CashflowStatementYFinance, company=cls.company, period=cls.period)
