from django.test import TestCase

from bfet import DataCreator, DjangoTestingModel

from src.currencies.models import Currency
from src.empresas.models import (
    BalanceSheetFinprep,
    BalanceSheetYahooQuery,
    BalanceSheetYFinance,
    CashflowStatementFinprep,
    CashflowStatementYahooQuery,
    CashflowStatementYFinance,
    Company,
    IncomeStatementFinprep,
    IncomeStatementYahooQuery,
    IncomeStatementYFinance,
)
from src.empresas.outils.average_statements import AverageStatements
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period


class TestAverageStatements(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DjangoTestingModel.create(Company)
        cls.period = DjangoTestingModel.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.currency = DjangoTestingModel.create(Currency)
        cls.revenue = DataCreator.create_random_float()
        cls.cost_of_revenue = DataCreator.create_random_float()
        cls.gross_profit = DataCreator.create_random_float()
        cls.research_and_development_expenses = DataCreator.create_random_float()
        cls.selling_general_and_administrative_expenses = DataCreator.create_random_float()
        cls.inc_st_finprep = DjangoTestingModel.create(
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
        cls.inc_st_yahooquery = DjangoTestingModel.create(
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
        cls.inc_st_yfinance = DjangoTestingModel.create(
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
        cls.bs_finprep = DjangoTestingModel.create(BalanceSheetFinprep, company=cls.company, period=cls.period)
        cls.bs_yahooquery = DjangoTestingModel.create(BalanceSheetYahooQuery, company=cls.company, period=cls.period)
        cls.bs_yfinance = DjangoTestingModel.create(BalanceSheetYFinance, company=cls.company, period=cls.period)
        cls.cf_st_finprep = DjangoTestingModel.create(CashflowStatementFinprep, company=cls.company, period=cls.period)
        cls.cf_st_yahooquery = DjangoTestingModel.create(
            CashflowStatementYahooQuery, company=cls.company, period=cls.period
        )
        cls.cf_st_yfinance = DjangoTestingModel.create(
            CashflowStatementYFinance, company=cls.company, period=cls.period
        )

    def test_find_correct_currency(self):
        pass

    def test_return_standard_keys(self):
        inc_st_finprep_keys = self.inc_st_finprep.return_standard().keys()
        inc_st_yahooquery_keys = self.inc_st_yahooquery.return_standard().keys()
        inc_st_yfinance_keys = self.inc_st_yfinance.return_standard().keys()
        bs_finprep_keys = self.bs_finprep.return_standard().keys()
        bs_yahooquery_keys = self.bs_yahooquery.return_standard().keys()
        bs_yfinance_keys = self.bs_yfinance.return_standard().keys()
        cf_st_finprep_keys = self.cf_st_finprep.return_standard().keys()
        cf_st_yahooquery_keys = self.cf_st_yahooquery.return_standard().keys()
        cf_st_yfinance_keys = self.cf_st_yfinance.return_standard().keys()
        assert inc_st_finprep_keys == inc_st_yahooquery_keys
        assert inc_st_finprep_keys == inc_st_yfinance_keys
        assert inc_st_yahooquery_keys == inc_st_yfinance_keys
        assert bs_finprep_keys == bs_yahooquery_keys
        assert bs_finprep_keys == bs_yfinance_keys
        assert bs_yahooquery_keys == bs_yfinance_keys
        assert cf_st_finprep_keys == cf_st_yahooquery_keys
        assert cf_st_finprep_keys == cf_st_yfinance_keys
        assert cf_st_yfinance_keys == cf_st_yahooquery_keys

    def test_return_standard_income_statement_keys(self):
        inc_st_finprep_keys = self.inc_st_finprep.return_standard().keys()
        assert ("revenue" in inc_st_finprep_keys)
        assert ("cost_of_revenue" in inc_st_finprep_keys)
        assert ("gross_profit" in inc_st_finprep_keys)
        assert ("rd_expenses" in inc_st_finprep_keys)
        assert ("general_administrative_expenses" in inc_st_finprep_keys)
        assert ("selling_marketing_expenses" in inc_st_finprep_keys)
        assert ("sga_expenses" in inc_st_finprep_keys)
        assert ("other_expenses" in inc_st_finprep_keys)
        assert ("operating_expenses" in inc_st_finprep_keys)
        assert ("cost_and_expenses" in inc_st_finprep_keys)
        assert ("interest_expense" in inc_st_finprep_keys)
        assert ("depreciation_amortization" in inc_st_finprep_keys)
        assert ("ebitda" in inc_st_finprep_keys)
        assert ("operating_income" in inc_st_finprep_keys)
        assert ("net_total_other_income_expenses" in inc_st_finprep_keys)
        assert ("income_before_tax" in inc_st_finprep_keys)
        assert ("income_tax_expenses" in inc_st_finprep_keys)
        assert ("net_income" in inc_st_finprep_keys)
        assert ("weighted_average_shares_outstanding" in inc_st_finprep_keys)
        assert ("weighted_average_diluated_shares_outstanding" in inc_st_finprep_keys)

    def test_return_standard_balance_sheet_keys(self):
        bs_finprep_keys = self.bs_finprep.return_standard().keys()
        assert ("cash_and_cash_equivalents" in bs_finprep_keys)
        assert ("short_term_investments" in bs_finprep_keys)
        assert ("cash_and_short_term_investments" in bs_finprep_keys)
        assert ("net_receivables" in bs_finprep_keys)
        assert ("inventory" in bs_finprep_keys)
        assert ("other_current_assets" in bs_finprep_keys)
        assert ("total_current_assets" in bs_finprep_keys)
        assert ("property_plant_equipment" in bs_finprep_keys)
        assert ("goodwill" in bs_finprep_keys)
        assert ("intangible_assets" in bs_finprep_keys)
        assert ("goodwill_and_intangible_assets" in bs_finprep_keys)
        assert ("long_term_investments" in bs_finprep_keys)
        assert ("tax_assets" in bs_finprep_keys)
        assert ("other_non_current_assets" in bs_finprep_keys)
        assert ("total_non_current_assets" in bs_finprep_keys)
        assert ("other_assets" in bs_finprep_keys)
        assert ("total_assets" in bs_finprep_keys)
        assert ("accounts_payable" in bs_finprep_keys)
        assert ("short_term_debt" in bs_finprep_keys)
        assert ("tax_payables" in bs_finprep_keys)
        assert ("deferred_revenue" in bs_finprep_keys)
        assert ("other_current_liabilities" in bs_finprep_keys)
        assert ("total_current_liabilities" in bs_finprep_keys)
        assert ("long_term_debt" in bs_finprep_keys)
        assert ("deferred_revenue_non_current" in bs_finprep_keys)
        assert ("deferred_tax_liabilities_non_current" in bs_finprep_keys)
        assert ("other_non_current_liabilities" in bs_finprep_keys)
        assert ("total_non_current_liabilities" in bs_finprep_keys)
        assert ("other_liabilities" in bs_finprep_keys)
        assert ("total_liabilities" in bs_finprep_keys)
        assert ("common_stocks" in bs_finprep_keys)
        assert ("retained_earnings" in bs_finprep_keys)
        assert ("accumulated_other_comprehensive_income_loss" in bs_finprep_keys)
        assert ("othertotal_stockholders_equity" in bs_finprep_keys)
        assert ("total_stockholders_equity" in bs_finprep_keys)
        assert ("total_liabilities_and_total_equity" in bs_finprep_keys)
        assert ("total_investments" in bs_finprep_keys)
        assert ("total_debt" in bs_finprep_keys)
        assert ("net_debt" in bs_finprep_keys)

    def test_return_standard_cashflow_statement_keys(self):
        cf_st_finprep_keys = self.cf_st_finprep.return_standard().keys()
        assert ("net_income" in cf_st_finprep_keys)
        assert ("depreciation_amortization" in cf_st_finprep_keys)
        assert ("deferred_income_tax" in cf_st_finprep_keys)
        assert ("stock_based_compensation" in cf_st_finprep_keys)
        assert ("change_in_working_capital" in cf_st_finprep_keys)
        assert ("accounts_receivable" in cf_st_finprep_keys)
        assert ("inventory" in cf_st_finprep_keys)
        assert ("accounts_payable" in cf_st_finprep_keys)
        assert ("other_working_capital" in cf_st_finprep_keys)
        assert ("other_non_cash_items" in cf_st_finprep_keys)
        assert ("operating_activities_cf" in cf_st_finprep_keys)
        assert ("investments_property_plant_equipment" in cf_st_finprep_keys)
        assert ("acquisitions_net" in cf_st_finprep_keys)
        assert ("purchases_investments" in cf_st_finprep_keys)
        assert ("sales_maturities_investments" in cf_st_finprep_keys)
        assert ("other_investing_activites" in cf_st_finprep_keys)
        assert ("investing_activities_cf" in cf_st_finprep_keys)
        assert ("debt_repayment" in cf_st_finprep_keys)
        assert ("common_stock_issued" in cf_st_finprep_keys)
        assert ("common_stock_repurchased" in cf_st_finprep_keys)
        assert ("dividends_paid" in cf_st_finprep_keys)
        assert ("other_financing_activities" in cf_st_finprep_keys)
        assert ("financing_activities_cf" in cf_st_finprep_keys)
        assert ("effect_forex_exchange" in cf_st_finprep_keys)
        assert ("net_change_cash" in cf_st_finprep_keys)
        assert ("cash_end_period" in cf_st_finprep_keys)
        assert ("cash_beginning_period" in cf_st_finprep_keys)
        assert ("operating_cf" in cf_st_finprep_keys)
        assert ("capex" in cf_st_finprep_keys)
        assert ("fcf" in cf_st_finprep_keys)

    def test_calculate_average_income_statement(self):
        average = AverageStatements(self.company).calculate_average_income_statement(self.period)
        assert type(average) == dict
        assert self.revenue == average["revenue"]
        assert self.cost_of_revenue == average["cost_of_revenue"]
        assert self.gross_profit == average["gross_profit"]
        assert self.research_and_development_expenses == average["rd_expenses"]
        assert self.selling_general_and_administrative_expenses == average["sga_expenses"]
        assert self.period.id == average["period_id"]
        assert self.period.year == average["date"]
        assert self.currency.id == average["reported_currency_id"]
