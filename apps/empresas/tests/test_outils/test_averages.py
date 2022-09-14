from django.test import TestCase

from bfet import DjangoTestingModel as DTM

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


class TestAverageStatements(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(
            Company,
        )
        cls.inc_st_finprep = DTM.create(IncomeStatementFinprep)
        cls.inc_st_yahooquery = DTM.create(IncomeStatementYahooQuery)
        cls.inc_st_yfinance = DTM.create(IncomeStatementYFinance)
        cls.bs_finprep = DTM.create(BalanceSheetFinprep)
        cls.bs_yahooquery = DTM.create(BalanceSheetYahooQuery)
        cls.bs_yfinance = DTM.create(BalanceSheetYFinance)
        cls.cf_st_finprep = DTM.create(CashflowStatementFinprep)
        cls.cf_st_yahooquery = DTM.create(CashflowStatementYahooQuery)
        cls.cf_st_yfinance = DTM.create(CashflowStatementYFinance)
    
    def test_return_standard_keys(self):
        inc_st_finprep_keys = self.inc_st_finprep.return_standard.keys()
        inc_st_yahooquery_keys = self.inc_st_yahooquery.return_standard.keys()
        inc_st_yfinance_keys = self.inc_st_yfinance.return_standard.keys()
        bs_finprep_keys = self.bs_finprep.return_standard.keys()
        bs_yahooquery_keys = self.bs_yahooquery.return_standard.keys()
        bs_yfinance_keys = self.bs_yfinance.return_standard.keys()
        cf_st_finprep_keys = self.cf_st_finprep.return_standard.keys()
        cf_st_yahooquery_keys = self.cf_st_yahooquery.return_standard.keys()
        cf_st_yfinance_keys = self.cf_st_yfinance.return_standard.keys()
        self.assertEqual(inc_st_finprep_keys, inc_st_yahooquery_keys)
        self.assertEqual(inc_st_finprep_keys, inc_st_yfinance_keys)
        self.assertEqual(inc_st_yahooquery_keys, inc_st_yfinance_keys)
        self.assertEqual(bs_finprep_keys, bs_yahooquery_keys)
        self.assertEqual(bs_finprep_keys, bs_yfinance_keys)
        self.assertEqual(bs_yahooquery_keys, bs_yfinance_keys)
        self.assertEqual(cf_st_finprep_keys, cf_st_yahooquery_keys)
        self.assertEqual(cf_st_finprep_keys, cf_st_yfinance_keys)
        self.assertEqual(cf_st_yfinance_keys, cf_st_yahooquery_keys)
        
    def test_return_standard_income_statement_keys(self):
        inc_st_finprep_keys = self.inc_st_finprep.return_standard.keys()
        self.assertTrue("revenue" in inc_st_finprep_keys)
        self.assertTrue("cost_of_revenue" in inc_st_finprep_keys)
        self.assertTrue("gross_profit" in inc_st_finprep_keys)
        self.assertTrue("rd_expenses" in inc_st_finprep_keys)
        self.assertTrue("general_administrative_expenses" in inc_st_finprep_keys)
        self.assertTrue("selling_marketing_expenses" in inc_st_finprep_keys)
        self.assertTrue("sga_expenses" in inc_st_finprep_keys)
        self.assertTrue("other_expenses" in inc_st_finprep_keys)
        self.assertTrue("operating_expenses" in inc_st_finprep_keys)
        self.assertTrue("cost_and_expenses" in inc_st_finprep_keys)
        self.assertTrue("interest_expense" in inc_st_finprep_keys)
        self.assertTrue("depreciation_amortization" in inc_st_finprep_keys)
        self.assertTrue("ebitda" in inc_st_finprep_keys)
        self.assertTrue("operating_income" in inc_st_finprep_keys)
        self.assertTrue("net_total_other_income_expenses" in inc_st_finprep_keys)
        self.assertTrue("income_before_tax" in inc_st_finprep_keys)
        self.assertTrue("income_tax_expenses" in inc_st_finprep_keys)
        self.assertTrue("net_income" in inc_st_finprep_keys)
        self.assertTrue("weighted_average_shares_outstanding" in inc_st_finprep_keys)
        self.assertTrue("weighted_average_diluated_shares_outstanding" in inc_st_finprep_keys)
    
    def test_return_standard_balance_sheet_keys(self):
        bs_finprep_keys = self.bs_finprep.return_standard.keys()
        self.assertTrue("cash_and_cash_equivalents" in bs_finprep_keys)
        self.assertTrue("short_term_investments" in bs_finprep_keys)
        self.assertTrue("cash_and_short_term_investments" in bs_finprep_keys)
        self.assertTrue("net_receivables" in bs_finprep_keys)
        self.assertTrue("inventory" in bs_finprep_keys)
        self.assertTrue("other_current_assets" in bs_finprep_keys)
        self.assertTrue("total_current_assets" in bs_finprep_keys)
        self.assertTrue("property_plant_equipment" in bs_finprep_keys)
        self.assertTrue("goodwill" in bs_finprep_keys)
        self.assertTrue("intangible_assets" in bs_finprep_keys)
        self.assertTrue("goodwill_and_intangible_assets" in bs_finprep_keys)
        self.assertTrue("long_term_investments" in bs_finprep_keys)
        self.assertTrue("tax_assets" in bs_finprep_keys)
        self.assertTrue("other_non_current_assets" in bs_finprep_keys)
        self.assertTrue("total_non_current_assets" in bs_finprep_keys)
        self.assertTrue("other_assets" in bs_finprep_keys)
        self.assertTrue("total_assets" in bs_finprep_keys)
        self.assertTrue("account_payables" in bs_finprep_keys)
        self.assertTrue("short_term_debt" in bs_finprep_keys)
        self.assertTrue("tax_payables" in bs_finprep_keys)
        self.assertTrue("deferred_revenue" in bs_finprep_keys)
        self.assertTrue("other_current_liabilities" in bs_finprep_keys)
        self.assertTrue("total_current_liabilities" in bs_finprep_keys)
        self.assertTrue("long_term_debt" in bs_finprep_keys)
        self.assertTrue("deferred_revenue_non_current" in bs_finprep_keys)
        self.assertTrue("deferred_tax_liabilities_non_current" in bs_finprep_keys)
        self.assertTrue("other_non_current_liabilities" in bs_finprep_keys)
        self.assertTrue("total_non_current_liabilities" in bs_finprep_keys)
        self.assertTrue("other_liabilities" in bs_finprep_keys)
        self.assertTrue("total_liabilities" in bs_finprep_keys)
        self.assertTrue("common_stocks" in bs_finprep_keys)
        self.assertTrue("retained_earnings" in bs_finprep_keys)
        self.assertTrue("accumulated_other_comprehensive_income_loss" in bs_finprep_keys)
        self.assertTrue("othertotal_stockholders_equity" in bs_finprep_keys)
        self.assertTrue("total_stockholders_equity" in bs_finprep_keys)
        self.assertTrue("total_liabilities_and_total_equity" in bs_finprep_keys)
        self.assertTrue("total_investments" in bs_finprep_keys)
        self.assertTrue("total_debt" in bs_finprep_keys)
        self.assertTrue("net_debt" in bs_finprep_keys)
    
    def test_return_standard_cashflow_statement_keys(self):
        cf_st_finprep_keys = self.cf_st_finprep.return_standard.keys()
        self.assertTrue("net_income" in cf_st_finprep_keys)
        self.assertTrue("depreciation_amortization" in cf_st_finprep_keys)
        self.assertTrue("deferred_income_tax" in cf_st_finprep_keys)
        self.assertTrue("stock_based_compesation" in cf_st_finprep_keys)
        self.assertTrue("change_in_working_capital" in cf_st_finprep_keys)
        self.assertTrue("accounts_receivables" in cf_st_finprep_keys)
        self.assertTrue("inventory" in cf_st_finprep_keys)
        self.assertTrue("accounts_payable" in cf_st_finprep_keys)
        self.assertTrue("other_working_capital" in cf_st_finprep_keys)
        self.assertTrue("other_non_cash_items" in cf_st_finprep_keys)
        self.assertTrue("operating_activities_cf" in cf_st_finprep_keys)
        self.assertTrue("investments_property_plant_equipment" in cf_st_finprep_keys)
        self.assertTrue("acquisitions_net" in cf_st_finprep_keys)
        self.assertTrue("purchases_investments" in cf_st_finprep_keys)
        self.assertTrue("sales_maturities_investments" in cf_st_finprep_keys)
        self.assertTrue("other_investing_activites" in cf_st_finprep_keys)
        self.assertTrue("investing_activities_cf" in cf_st_finprep_keys)
        self.assertTrue("debt_repayment" in cf_st_finprep_keys)
        self.assertTrue("common_stock_issued" in cf_st_finprep_keys)
        self.assertTrue("common_stock_repurchased" in cf_st_finprep_keys)
        self.assertTrue("dividends_paid" in cf_st_finprep_keys)
        self.assertTrue("other_financing_activities" in cf_st_finprep_keys)
        self.assertTrue("financing_activities_cf" in cf_st_finprep_keys)
        self.assertTrue("effect_forex_exchange" in cf_st_finprep_keys)
        self.assertTrue("net_change_cash" in cf_st_finprep_keys)
        self.assertTrue("cash_end_period" in cf_st_finprep_keys)
        self.assertTrue("cash_beginning_period" in cf_st_finprep_keys)
        self.assertTrue("operating_cf" in cf_st_finprep_keys)
        self.assertTrue("capex" in cf_st_finprep_keys)
        self.assertTrue("fcf" in cf_st_finprep_keys)
        