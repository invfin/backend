from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.general.constants import PERIOD_FOR_YEAR
from apps.general.models import Period
from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
)


class TestAverageStatementsYahooQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(Company)
        cls.period = DTM.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.inc_st_yahooquery = DTM.create(IncomeStatementYahooQuery, company=cls.company, period=cls.period)
        cls.bs_yahooquery = DTM.create(BalanceSheetYahooQuery, company=cls.company, period=cls.period)
        cls.cf_st_yahooquery = DTM.create(CashflowStatementYahooQuery, company=cls.company, period=cls.period)

    def test_return_standard_income_statement(self):
        inc_st_yahooquery_dict = self.inc_st_yahooquery.return_standard
        self.assertEqual(inc_st_yahooquery_dict["revenue"], self.inc_st_yahooquery.total_revenue)
        self.assertEqual(inc_st_yahooquery_dict["cost_of_revenue"], self.inc_st_yahooquery.reconciled_cost_of_revenue)
        self.assertEqual(inc_st_yahooquery_dict["gross_profit"], self.inc_st_yahooquery.gross_profit)
        self.assertEqual(inc_st_yahooquery_dict["rd_expenses"], self.inc_st_yahooquery.research_and_development)
        self.assertEqual(inc_st_yahooquery_dict["general_administrative_expenses"], None)
        self.assertEqual(inc_st_yahooquery_dict["selling_marketing_expenses"], None)
        self.assertEqual(
            inc_st_yahooquery_dict["sga_expenses"], self.inc_st_yahooquery.selling_general_and_administration
        )
        self.assertEqual(inc_st_yahooquery_dict["other_expenses"], self.inc_st_yahooquery.other_income_expense)
        self.assertEqual(inc_st_yahooquery_dict["operating_expenses"], self.inc_st_yahooquery.operating_expense)
        self.assertEqual(inc_st_yahooquery_dict["cost_and_expenses"], self.inc_st_yahooquery.total_expenses)
        self.assertEqual(
            inc_st_yahooquery_dict["interest_expense"], self.inc_st_yahooquery.interest_expense_non_operating
        )
        self.assertEqual(
            inc_st_yahooquery_dict["depreciation_amortization"], self.inc_st_yahooquery.reconciled_depreciation
        )
        self.assertEqual(inc_st_yahooquery_dict["ebitda"], self.inc_st_yahooquery.normalized_ebitda)
        self.assertEqual(
            inc_st_yahooquery_dict["operating_income"], self.inc_st_yahooquery.total_operating_income_as_reported
        )
        self.assertEqual(
            inc_st_yahooquery_dict["net_total_other_income_expenses"], self.inc_st_yahooquery.operating_expense
        )
        self.assertEqual(inc_st_yahooquery_dict["income_before_tax"], self.inc_st_yahooquery.pretax_income)
        self.assertEqual(inc_st_yahooquery_dict["income_tax_expenses"], self.inc_st_yahooquery.tax_provision)
        self.assertEqual(inc_st_yahooquery_dict["net_income"], self.inc_st_yahooquery.normalized_income)
        self.assertEqual(
            inc_st_yahooquery_dict["weighted_average_shares_outstanding"], self.inc_st_yahooquery.basic_average_shares
        )
        self.assertEqual(
            inc_st_yahooquery_dict["weighted_average_diluated_shares_outstanding"],
            self.inc_st_yahooquery.diluted_average_shares,
        )

    def test_return_standard_balance_sheet(self):
        bs_yahooquery_dict = self.bs_yahooquery.return_standard
        self.assertEqual(bs_yahooquery_dict["cash_and_cash_equivalents"], self.bs_yahooquery.cash_and_cash_equivalents)
        self.assertEqual(bs_yahooquery_dict["short_term_investments"], self.bs_yahooquery.other_short_term_investments)
        self.assertEqual(
            bs_yahooquery_dict["cash_and_short_term_investments"],
            self.bs_yahooquery.cash_cash_equivalents_and_short_term_investments,
        )
        self.assertEqual(bs_yahooquery_dict["net_receivables"], self.bs_yahooquery.receivables)
        self.assertEqual(bs_yahooquery_dict["inventory"], self.bs_yahooquery.inventory)
        self.assertEqual(bs_yahooquery_dict["other_current_assets"], self.bs_yahooquery.other_current_assets)
        self.assertEqual(bs_yahooquery_dict["total_current_assets"], self.bs_yahooquery.current_assets)
        self.assertEqual(bs_yahooquery_dict["property_plant_equipment"], self.bs_yahooquery.net_ppe)
        self.assertEqual(bs_yahooquery_dict["goodwill"], None)
        self.assertEqual(bs_yahooquery_dict["intangible_assets"], None)
        self.assertEqual(bs_yahooquery_dict["goodwill_and_intangible_assets"], None)
        self.assertEqual(bs_yahooquery_dict["long_term_investments"], self.bs_yahooquery.investments_and_advances)
        self.assertEqual(bs_yahooquery_dict["tax_assets"], None)
        self.assertEqual(bs_yahooquery_dict["other_non_current_assets"], self.bs_yahooquery.other_non_current_assets)
        self.assertEqual(bs_yahooquery_dict["total_non_current_assets"], self.bs_yahooquery.total_non_current_assets)
        self.assertEqual(bs_yahooquery_dict["other_assets"], None)
        self.assertEqual(bs_yahooquery_dict["total_assets"], self.bs_yahooquery.total_assets)
        self.assertEqual(bs_yahooquery_dict["account_payables"], self.bs_yahooquery.payables_and_accrued_expenses)
        self.assertEqual(
            bs_yahooquery_dict["short_term_debt"], self.bs_yahooquery.current_debt_and_capital_lease_obligation
        )
        self.assertEqual(bs_yahooquery_dict["tax_payables"], None)
        self.assertEqual(bs_yahooquery_dict["deferred_revenue"], self.bs_yahooquery.current_deferred_revenue)
        self.assertEqual(bs_yahooquery_dict["other_current_liabilities"], self.bs_yahooquery.other_current_liabilities)
        self.assertEqual(bs_yahooquery_dict["total_current_liabilities"], self.bs_yahooquery.current_liabilities)
        self.assertEqual(
            bs_yahooquery_dict["long_term_debt"], self.bs_yahooquery.long_term_debt_and_capital_lease_obligation
        )
        self.assertEqual(bs_yahooquery_dict["deferred_revenue_non_current"], None)
        self.assertEqual(bs_yahooquery_dict["deferred_tax_liabilities_non_current"], None)
        self.assertEqual(
            bs_yahooquery_dict["other_non_current_liabilities"], self.bs_yahooquery.other_non_current_liabilities
        )
        self.assertEqual(
            bs_yahooquery_dict["total_non_current_liabilities"],
            self.bs_yahooquery.total_non_current_liabilities_net_minority_interest,
        )
        self.assertEqual(bs_yahooquery_dict["other_liabilities"], None)
        self.assertEqual(
            bs_yahooquery_dict["total_liabilities"], self.bs_yahooquery.total_liabilities_net_minority_interest
        )
        self.assertEqual(bs_yahooquery_dict["common_stocks"], self.bs_yahooquery.common_stock)
        self.assertEqual(bs_yahooquery_dict["retained_earnings"], self.bs_yahooquery.retained_earnings)
        self.assertEqual(
            bs_yahooquery_dict["accumulated_other_comprehensive_income_loss"],
            self.bs_yahooquery.gains_losses_not_affecting_retained_earnings,
        )
        self.assertEqual(bs_yahooquery_dict["othertotal_stockholders_equity"], None)
        self.assertEqual(
            bs_yahooquery_dict["total_stockholders_equity"], self.bs_yahooquery.total_equity_gross_minority_interest
        )
        self.assertEqual(bs_yahooquery_dict["total_liabilities_and_total_equity"], self.bs_yahooquery.total_assets)
        self.assertEqual(bs_yahooquery_dict["total_investments"], None)
        self.assertEqual(bs_yahooquery_dict["total_debt"], self.bs_yahooquery.total_debt)
        self.assertEqual(bs_yahooquery_dict["net_debt"], self.bs_yahooquery.net_debt)

    def test_return_standard_cashflow_statement(self):
        cf_st_yahooquery_dict = self.cf_st_yahooquery.return_standard
        self.assertEqual(cf_st_yahooquery_dict["net_income"], self.cf_st_yahooquery.net_income)
        self.assertEqual(
            cf_st_yahooquery_dict["depreciation_amortization"], self.cf_st_yahooquery.depreciation_and_amortization
        )
        self.assertEqual(cf_st_yahooquery_dict["deferred_income_tax"], self.cf_st_yahooquery.deferred_income_tax)
        self.assertEqual(
            cf_st_yahooquery_dict["stock_based_compesation"], self.cf_st_yahooquery.stock_based_compensation
        )
        self.assertEqual(
            cf_st_yahooquery_dict["change_in_working_capital"], self.cf_st_yahooquery.change_in_working_capital
        )
        self.assertEqual(
            cf_st_yahooquery_dict["accounts_receivables"], self.cf_st_yahooquery.changes_in_account_receivables
        )
        self.assertEqual(cf_st_yahooquery_dict["inventory"], self.cf_st_yahooquery.change_in_inventory)
        self.assertEqual(cf_st_yahooquery_dict["accounts_payable"], None)
        self.assertEqual(
            cf_st_yahooquery_dict["other_working_capital"], self.cf_st_yahooquery.change_in_other_working_capital
        )
        self.assertEqual(cf_st_yahooquery_dict["other_non_cash_items"], self.cf_st_yahooquery.other_non_cash_items)
        self.assertEqual(
            cf_st_yahooquery_dict["operating_activities_cf"],
            self.cf_st_yahooquery.cash_flow_from_continuing_operating_activities,
        )
        self.assertEqual(cf_st_yahooquery_dict["investments_property_plant_equipment"], None)
        self.assertEqual(cf_st_yahooquery_dict["acquisitions_net"], self.cf_st_yahooquery.purchase_of_business)
        self.assertEqual(cf_st_yahooquery_dict["purchases_investments"], self.cf_st_yahooquery.purchase_of_investment)
        self.assertEqual(
            cf_st_yahooquery_dict["sales_maturities_investments"], self.cf_st_yahooquery.sale_of_investment
        )
        self.assertEqual(
            cf_st_yahooquery_dict["other_investing_activites"], self.cf_st_yahooquery.net_other_investing_changes
        )
        self.assertEqual(
            cf_st_yahooquery_dict["investing_activities_cf"],
            self.cf_st_yahooquery.cash_flow_from_continuing_investing_activities,
        )
        self.assertEqual(cf_st_yahooquery_dict["debt_repayment"], self.cf_st_yahooquery.repayment_of_debt)
        self.assertEqual(cf_st_yahooquery_dict["common_stock_issued"], self.cf_st_yahooquery.issuance_of_capital_stock)
        self.assertEqual(
            cf_st_yahooquery_dict["common_stock_repurchased"], self.cf_st_yahooquery.repurchase_of_capital_stock
        )
        self.assertEqual(cf_st_yahooquery_dict["dividends_paid"], self.cf_st_yahooquery.common_stock_dividend_paid)
        self.assertEqual(
            cf_st_yahooquery_dict["other_financing_activities"], self.cf_st_yahooquery.net_other_financing_charges
        )
        self.assertEqual(
            cf_st_yahooquery_dict["financing_activities_cf"],
            self.cf_st_yahooquery.cash_flow_from_continuing_financing_activities,
        )
        self.assertEqual(cf_st_yahooquery_dict["effect_forex_exchange"], None)
        self.assertEqual(cf_st_yahooquery_dict["net_change_cash"], None)
        self.assertEqual(cf_st_yahooquery_dict["cash_end_period"], self.cf_st_yahooquery.end_cash_position)
        self.assertEqual(cf_st_yahooquery_dict["cash_beginning_period"], self.cf_st_yahooquery.beginning_cash_position)
        self.assertEqual(cf_st_yahooquery_dict["operating_cf"], self.cf_st_yahooquery.operating_cash_flow)
        self.assertEqual(cf_st_yahooquery_dict["capex"], self.cf_st_yahooquery.capital_expenditure)
        self.assertEqual(cf_st_yahooquery_dict["fcf"], self.cf_st_yahooquery.free_cash_flow)
