from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from src.empresas.models import BalanceSheetYFinance, CashflowStatementYFinance, Company, IncomeStatementYFinance
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period


class TestAverageStatementsYFinance(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(Company)
        cls.period = DTM.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.inc_st_yfinance = DTM.create(IncomeStatementYFinance, company=cls.company, period=cls.period)
        cls.bs_yfinance = DTM.create(BalanceSheetYFinance, company=cls.company, period=cls.period)
        cls.cf_st_yfinance = DTM.create(CashflowStatementYFinance, company=cls.company, period=cls.period)

    def test_return_standard_income_statement(self):
        inc_st_yfinance_dict = self.inc_st_yfinance.return_standard
        inc_st_yfinance_dict["revenue"] = self.inc_st_yfinance.total_revenue
        inc_st_yfinance_dict["cost_of_revenue"] = self.inc_st_yfinance.cost_of_revenue
        inc_st_yfinance_dict["gross_profit"] = self.inc_st_yfinance.gross_profit
        inc_st_yfinance_dict["rd_expenses"] = self.inc_st_yfinance.research_development
        inc_st_yfinance_dict["general_administrative_expenses"] = None
        inc_st_yfinance_dict["selling_marketing_expenses"] = None
        inc_st_yfinance_dict["sga_expenses"] = self.inc_st_yfinance.selling_general_administrative
        inc_st_yfinance_dict["other_expenses"] = None
        inc_st_yfinance_dict["operating_expenses"] = None
        inc_st_yfinance_dict["cost_and_expenses"] = self.inc_st_yfinance.total_operating_expenses
        inc_st_yfinance_dict["interest_expense"] = None
        inc_st_yfinance_dict["depreciation_amortization"] = None
        inc_st_yfinance_dict["ebitda"] = None
        inc_st_yfinance_dict["operating_income"] = self.inc_st_yfinance.operating_income
        inc_st_yfinance_dict["net_total_other_income_expenses"] = None
        inc_st_yfinance_dict["income_before_tax"] = self.inc_st_yfinance.income_before_tax
        inc_st_yfinance_dict["income_tax_expenses"] = self.inc_st_yfinance.income_tax_expense
        inc_st_yfinance_dict["net_income"] = self.inc_st_yfinance.net_income_applicable_to_common_shares
        inc_st_yfinance_dict["weighted_average_shares_outstanding"] = None
        inc_st_yfinance_dict["weighted_average_diluated_shares_outstanding"] = None

    def test_return_standard_balance_sheet(self):
        bs_yfinance_dict = self.bs_yfinance.return_standard
        bs_yfinance_dict["cash_and_cash_equivalents"] = self.bs_yfinance.cash
        bs_yfinance_dict["short_term_investments"] = self.bs_yfinance.short_term_investments
        bs_yfinance_dict["cash_and_short_term_investments"] = None
        bs_yfinance_dict["net_receivables"] = self.bs_yfinance.net_receivables
        bs_yfinance_dict["inventory"] = self.bs_yfinance.inventory
        bs_yfinance_dict["other_current_assets"] = self.bs_yfinance.other_current_assets
        bs_yfinance_dict["total_current_assets"] = self.bs_yfinance.total_current_assets
        bs_yfinance_dict["property_plant_equipment"] = None
        bs_yfinance_dict["goodwill"] = None
        bs_yfinance_dict["intangible_assets"] = None
        bs_yfinance_dict["goodwill_and_intangible_assets"] = None
        bs_yfinance_dict["long_term_investments"] = self.bs_yfinance.long_term_investments
        bs_yfinance_dict["tax_assets"] = None
        bs_yfinance_dict["other_non_current_assets"] = None
        bs_yfinance_dict["total_non_current_assets"] = None
        bs_yfinance_dict["other_assets"] = None
        bs_yfinance_dict["total_assets"] = self.bs_yfinance.total_assets
        bs_yfinance_dict["account_payables"] = self.bs_yfinance.accounts_payable
        bs_yfinance_dict["short_term_debt"] = None
        bs_yfinance_dict["tax_payables"] = None
        bs_yfinance_dict["deferred_revenue"] = None
        bs_yfinance_dict["other_current_liabilities"] = None
        bs_yfinance_dict["total_current_liabilities"] = self.bs_yfinance.total_current_liabilities
        bs_yfinance_dict["long_term_debt"] = self.bs_yfinance.long_term_debt
        bs_yfinance_dict["deferred_revenue_non_current"] = None
        bs_yfinance_dict["deferred_tax_liabilities_non_current"] = None
        bs_yfinance_dict["other_non_current_liabilities"] = None
        bs_yfinance_dict["total_non_current_liabilities"] = None
        bs_yfinance_dict["other_liabilities"] = None
        bs_yfinance_dict["total_liabilities"] = self.bs_yfinance.total_liab
        bs_yfinance_dict["common_stocks"] = self.bs_yfinance.common_stock
        bs_yfinance_dict["retained_earnings"] = self.bs_yfinance.retained_earnings
        bs_yfinance_dict["accumulated_other_comprehensive_income_loss"] = None
        bs_yfinance_dict["othertotal_stockholders_equity"] = None
        bs_yfinance_dict["total_stockholders_equity"] = self.bs_yfinance.total_stockholder_equity
        bs_yfinance_dict["total_liabilities_and_total_equity"] = self.bs_yfinance.total_assets
        bs_yfinance_dict["total_investments"] = None
        bs_yfinance_dict["total_debt"] = None
        bs_yfinance_dict["net_debt"] = None

    def test_return_standard_cashflow_statement(self):
        cf_st_yfinance_dict = self.cf_st_yfinance.return_standard
        cf_st_yfinance_dict["net_income"] = self.cf_st_yfinance.net_income
        cf_st_yfinance_dict["depreciation_amortization"] = self.cf_st_yfinance.depreciation
        cf_st_yfinance_dict["deferred_income_tax"] = None
        cf_st_yfinance_dict["stock_based_compesation"] = None
        cf_st_yfinance_dict["change_in_working_capital"] = None
        cf_st_yfinance_dict["accounts_receivables"] = self.cf_st_yfinance.change_to_account_receivables
        cf_st_yfinance_dict["inventory"] = self.cf_st_yfinance.change_to_inventory
        cf_st_yfinance_dict["accounts_payable"] = None
        cf_st_yfinance_dict["other_working_capital"] = None
        cf_st_yfinance_dict["other_non_cash_items"] = None
        cf_st_yfinance_dict["operating_activities_cf"] = None
        cf_st_yfinance_dict["investments_property_plant_equipment"] = None
        cf_st_yfinance_dict["acquisitions_net"] = None
        cf_st_yfinance_dict["purchases_investments"] = None
        cf_st_yfinance_dict["sales_maturities_investments"] = None
        cf_st_yfinance_dict["other_investing_activites"] = self.cf_st_yfinance.other_cashflows_from_investing_activities
        cf_st_yfinance_dict["investing_activities_cf"] = None
        cf_st_yfinance_dict["debt_repayment"] = None
        cf_st_yfinance_dict["common_stock_issued"] = self.cf_st_yfinance.issuance_of_stock
        cf_st_yfinance_dict["common_stock_repurchased"] = None
        cf_st_yfinance_dict["dividends_paid"] = self.cf_st_yfinance.dividends_paid
        cf_st_yfinance_dict["other_financing_activities"] = None
        cf_st_yfinance_dict["financing_activities_cf"] = None
        cf_st_yfinance_dict["effect_forex_exchange"] = None
        cf_st_yfinance_dict["net_change_cash"] = None
        cf_st_yfinance_dict["cash_end_period"] = None
        cf_st_yfinance_dict["cash_beginning_period"] = None
        cf_st_yfinance_dict["operating_cf"] = None
        cf_st_yfinance_dict["capex"] = self.cf_st_yfinance.capital_expenditures
        cf_st_yfinance_dict["fcf"] = None
