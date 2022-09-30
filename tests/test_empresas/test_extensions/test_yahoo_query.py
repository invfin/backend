import pytest

from bfet import DjangoTestingModel as DTM

from apps.general.constants import PERIOD_FOR_YEAR
from apps.general.models import Period
from apps.empresas.models import (
    Company,
    IncomeStatementYahooQuery,
    BalanceSheetYahooQuery,
    CashflowStatementYahooQuery,
)


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestAverageStatementsYahooQuery:
    @classmethod
    def setup_class(cls):
        cls.company = DTM.create(Company)
        cls.period = DTM.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.inc_st_yahooquery = DTM.create(IncomeStatementYahooQuery, company=cls.company, period=cls.period)
        cls.bs_yahooquery = DTM.create(BalanceSheetYahooQuery, company=cls.company, period=cls.period)
        cls.cf_st_yahooquery = DTM.create(CashflowStatementYahooQuery, company=cls.company, period=cls.period)

    def test_return_standard_income_statement(self):
        inc_st_yahooquery_dict = self.inc_st_yahooquery.return_standard
        assert inc_st_yahooquery_dict["revenue"] == self.inc_st_yahooquery.total_revenue
        assert inc_st_yahooquery_dict["cost_of_revenue"] == self.inc_st_yahooquery.reconciled_cost_of_revenue
        assert inc_st_yahooquery_dict["gross_profit"] == self.inc_st_yahooquery.gross_profit
        assert inc_st_yahooquery_dict["rd_expenses"] == self.inc_st_yahooquery.research_and_development
        assert inc_st_yahooquery_dict["general_administrative_expenses"] == None
        assert inc_st_yahooquery_dict["selling_marketing_expenses"] == None
        assert inc_st_yahooquery_dict["sga_expenses"] == self.inc_st_yahooquery.selling_general_and_administration
        assert inc_st_yahooquery_dict["other_expenses"] == self.inc_st_yahooquery.other_income_expense
        assert inc_st_yahooquery_dict["operating_expenses"] == self.inc_st_yahooquery.operating_expense
        assert inc_st_yahooquery_dict["cost_and_expenses"] == self.inc_st_yahooquery.total_expenses
        assert inc_st_yahooquery_dict["interest_expense"] == self.inc_st_yahooquery.interest_expense_non_operating
        assert inc_st_yahooquery_dict["depreciation_amortization"] == self.inc_st_yahooquery.reconciled_depreciation
        assert inc_st_yahooquery_dict["ebitda"] == self.inc_st_yahooquery.normalized_ebitda
        assert inc_st_yahooquery_dict["operating_income"] == self.inc_st_yahooquery.total_operating_income_as_reported
        assert inc_st_yahooquery_dict["net_total_other_income_expenses"] == self.inc_st_yahooquery.operating_expense
        assert inc_st_yahooquery_dict["income_before_tax"] == self.inc_st_yahooquery.pretax_income
        assert inc_st_yahooquery_dict["income_tax_expenses"] == self.inc_st_yahooquery.tax_provision
        assert inc_st_yahooquery_dict["net_income"] == self.inc_st_yahooquery.normalized_income
        assert (
            inc_st_yahooquery_dict["weighted_average_shares_outstanding"] == self.inc_st_yahooquery.basic_average_shares
        )
        assert (
            inc_st_yahooquery_dict["weighted_average_diluated_shares_outstanding"]
            == self.inc_st_yahooquery.diluted_average_shares,
        )

    def test_return_standard_balance_sheet(self):
        bs_yahooquery_dict = self.bs_yahooquery.return_standard
        assert bs_yahooquery_dict["cash_and_cash_equivalents"] == self.bs_yahooquery.cash_and_cash_equivalents
        assert bs_yahooquery_dict["short_term_investments"] == self.bs_yahooquery.other_short_term_investments
        assert (
            bs_yahooquery_dict["cash_and_short_term_investments"]
            == self.bs_yahooquery.cash_cash_equivalents_and_short_term_investments,
        )
        assert bs_yahooquery_dict["net_receivables"] == self.bs_yahooquery.receivables
        assert bs_yahooquery_dict["inventory"] == self.bs_yahooquery.inventory
        assert bs_yahooquery_dict["other_current_assets"] == self.bs_yahooquery.other_current_assets
        assert bs_yahooquery_dict["total_current_assets"] == self.bs_yahooquery.current_assets
        assert bs_yahooquery_dict["property_plant_equipment"] == self.bs_yahooquery.net_ppe
        assert bs_yahooquery_dict["goodwill"] == None
        assert bs_yahooquery_dict["intangible_assets"] == None
        assert bs_yahooquery_dict["goodwill_and_intangible_assets"] == None
        assert bs_yahooquery_dict["long_term_investments"] == self.bs_yahooquery.investments_and_advances
        assert bs_yahooquery_dict["tax_assets"] == None
        assert bs_yahooquery_dict["other_non_current_assets"] == self.bs_yahooquery.other_non_current_assets
        assert bs_yahooquery_dict["total_non_current_assets"] == self.bs_yahooquery.total_non_current_assets
        assert (bs_yahooquery_dict["other_assets"], None)
        assert bs_yahooquery_dict["total_assets"] == self.bs_yahooquery.total_assets
        assert bs_yahooquery_dict["account_payables"] == self.bs_yahooquery.payables_and_accrued_expenses
        assert bs_yahooquery_dict["short_term_debt"] == self.bs_yahooquery.current_debt_and_capital_lease_obligation
        assert bs_yahooquery_dict["tax_payables"] == None
        assert bs_yahooquery_dict["deferred_revenue"] == self.bs_yahooquery.current_deferred_revenue
        assert bs_yahooquery_dict["other_current_liabilities"] == self.bs_yahooquery.other_current_liabilities
        assert bs_yahooquery_dict["total_current_liabilities"] == self.bs_yahooquery.current_liabilities
        assert bs_yahooquery_dict["long_term_debt"] == self.bs_yahooquery.long_term_debt_and_capital_lease_obligation
        assert bs_yahooquery_dict["deferred_revenue_non_current"] == None
        assert bs_yahooquery_dict["deferred_tax_liabilities_non_current"] == None
        assert bs_yahooquery_dict["other_non_current_liabilities"] == self.bs_yahooquery.other_non_current_liabilities
        assert (
            bs_yahooquery_dict["total_non_current_liabilities"]
            == self.bs_yahooquery.total_non_current_liabilities_net_minority_interest,
        )
        assert bs_yahooquery_dict["other_liabilities"] == None
        assert bs_yahooquery_dict["total_liabilities"] == self.bs_yahooquery.total_liabilities_net_minority_interest
        assert bs_yahooquery_dict["common_stocks"] == self.bs_yahooquery.common_stock
        assert bs_yahooquery_dict["retained_earnings"] == self.bs_yahooquery.retained_earnings
        assert (
            bs_yahooquery_dict["accumulated_other_comprehensive_income_loss"]
            == self.bs_yahooquery.gains_losses_not_affecting_retained_earnings,
        )
        assert bs_yahooquery_dict["othertotal_stockholders_equity"] == None
        assert (
            bs_yahooquery_dict["total_stockholders_equity"] == self.bs_yahooquery.total_equity_gross_minority_interest
        )
        assert bs_yahooquery_dict["total_liabilities_and_total_equity"] == self.bs_yahooquery.total_assets
        assert bs_yahooquery_dict["total_investments"] == None
        assert bs_yahooquery_dict["total_debt"] == self.bs_yahooquery.total_debt
        assert bs_yahooquery_dict["net_debt"] == self.bs_yahooquery.net_debt

    def test_return_standard_cashflow_statement(self):
        cf_st_yahooquery_dict = self.cf_st_yahooquery.return_standard
        assert cf_st_yahooquery_dict["net_income"] == self.cf_st_yahooquery.net_income
        assert cf_st_yahooquery_dict["depreciation_amortization"] == self.cf_st_yahooquery.depreciation_and_amortization
        assert cf_st_yahooquery_dict["deferred_income_tax"] == self.cf_st_yahooquery.deferred_income_tax
        assert cf_st_yahooquery_dict["stock_based_compesation"] == self.cf_st_yahooquery.stock_based_compensation
        assert cf_st_yahooquery_dict["change_in_working_capital"] == self.cf_st_yahooquery.change_in_working_capital
        assert cf_st_yahooquery_dict["accounts_receivables"] == self.cf_st_yahooquery.changes_in_account_receivables
        assert cf_st_yahooquery_dict["inventory"] == self.cf_st_yahooquery.change_in_inventory
        assert cf_st_yahooquery_dict["accounts_payable"] == None
        assert cf_st_yahooquery_dict["other_working_capital"] == self.cf_st_yahooquery.change_in_other_working_capital
        assert cf_st_yahooquery_dict["other_non_cash_items"] == self.cf_st_yahooquery.other_non_cash_items
        assert (
            cf_st_yahooquery_dict["operating_activities_cf"]
            == self.cf_st_yahooquery.cash_flow_from_continuing_operating_activities,
        )
        assert cf_st_yahooquery_dict["investments_property_plant_equipment"] == None
        assert cf_st_yahooquery_dict["acquisitions_net"] == self.cf_st_yahooquery.purchase_of_business
        assert cf_st_yahooquery_dict["purchases_investments"] == self.cf_st_yahooquery.purchase_of_investment
        assert cf_st_yahooquery_dict["sales_maturities_investments"] == self.cf_st_yahooquery.sale_of_investment
        assert cf_st_yahooquery_dict["other_investing_activites"] == self.cf_st_yahooquery.net_other_investing_changes
        assert (
            cf_st_yahooquery_dict["investing_activities_cf"]
            == self.cf_st_yahooquery.cash_flow_from_continuing_investing_activities,
        )
        assert cf_st_yahooquery_dict["debt_repayment"] == self.cf_st_yahooquery.repayment_of_debt
        assert cf_st_yahooquery_dict["common_stock_issued"] == self.cf_st_yahooquery.issuance_of_capital_stock
        assert cf_st_yahooquery_dict["common_stock_repurchased"] == self.cf_st_yahooquery.repurchase_of_capital_stock
        assert cf_st_yahooquery_dict["dividends_paid"] == self.cf_st_yahooquery.common_stock_dividend_paid
        assert cf_st_yahooquery_dict["other_financing_activities"] == self.cf_st_yahooquery.net_other_financing_charges
        assert (
            cf_st_yahooquery_dict["financing_activities_cf"]
            == self.cf_st_yahooquery.cash_flow_from_continuing_financing_activities,
        )
        assert cf_st_yahooquery_dict["effect_forex_exchange"] == None
        assert cf_st_yahooquery_dict["net_change_cash"] == None
        assert cf_st_yahooquery_dict["cash_end_period"] == self.cf_st_yahooquery.end_cash_position
        assert cf_st_yahooquery_dict["cash_beginning_period"] == self.cf_st_yahooquery.beginning_cash_position
        assert cf_st_yahooquery_dict["operating_cf"] == self.cf_st_yahooquery.operating_cash_flow
        assert cf_st_yahooquery_dict["capex"] == self.cf_st_yahooquery.capital_expenditure
        assert cf_st_yahooquery_dict["fcf"] == self.cf_st_yahooquery.free_cash_flow
