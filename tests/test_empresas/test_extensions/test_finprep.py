from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.periods.constants import PERIOD_FOR_YEAR
from apps.periods.models import Period
from apps.empresas.models import (
    Company,
    IncomeStatementFinprep,
    BalanceSheetFinprep,
    CashflowStatementFinprep,
)


class TestAverageStatementsFinprep(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DTM.create(Company)
        cls.period = DTM.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.inc_st_finprep = DTM.create(IncomeStatementFinprep, company=cls.company, period=cls.period)
        cls.bs_finprep = DTM.create(BalanceSheetFinprep, company=cls.company, period=cls.period)
        cls.cf_st_finprep = DTM.create(CashflowStatementFinprep, company=cls.company, period=cls.period)

    def test_return_standard_income_statement(self):
        inc_st_finprep_dict = self.inc_st_finprep.return_standard
        assert self.inc_st_finprep.revenue == inc_st_finprep_dict["revenue"]
        assert self.inc_st_finprep.cost_of_revenue == inc_st_finprep_dict["cost_of_revenue"]
        assert self.inc_st_finprep.gross_profit == inc_st_finprep_dict["gross_profit"]
        assert self.inc_st_finprep.research_and_development_expenses == inc_st_finprep_dict["rd_expenses"]
        assert (
            self.inc_st_finprep.general_and_administrative_expenses
            == inc_st_finprep_dict["general_administrative_expenses"]
        )
        assert self.inc_st_finprep.selling_and_marketing_expenses == inc_st_finprep_dict["selling_marketing_expenses"]
        assert self.inc_st_finprep.selling_general_and_administrative_expenses == inc_st_finprep_dict["sga_expenses"]
        assert self.inc_st_finprep.other_expenses == inc_st_finprep_dict["other_expenses"]
        assert self.inc_st_finprep.operating_expenses == inc_st_finprep_dict["operating_expenses"]
        assert self.inc_st_finprep.cost_and_expenses == inc_st_finprep_dict["cost_and_expenses"]
        assert self.inc_st_finprep.interest_expense == inc_st_finprep_dict["interest_expense"]
        assert self.inc_st_finprep.depreciation_and_amortization == inc_st_finprep_dict["depreciation_amortization"]
        assert self.inc_st_finprep.ebitda == inc_st_finprep_dict["ebitda"]
        assert self.inc_st_finprep.operating_income == inc_st_finprep_dict["operating_income"]
        assert (
            self.inc_st_finprep.total_other_income_expenses_net
            == inc_st_finprep_dict["net_total_other_income_expenses"]
        )
        assert self.inc_st_finprep.income_before_tax == inc_st_finprep_dict["income_before_tax"]
        assert self.inc_st_finprep.income_tax_expense == inc_st_finprep_dict["income_tax_expenses"]
        assert self.inc_st_finprep.net_income == inc_st_finprep_dict["net_income"]
        assert (
            self.inc_st_finprep.weighted_average_shs_out == inc_st_finprep_dict["weighted_average_shares_outstanding"]
        )
        assert (
            self.inc_st_finprep.weighted_average_shs_out_dil
            == inc_st_finprep_dict["weighted_average_diluated_shares_outstanding"]
        )

    def test_return_standard_balance_sheet(self):
        bs_finprep_dict = self.bs_finprep.return_standard
        assert self.bs_finprep.cash_and_cash_equivalents == bs_finprep_dict["cash_and_cash_equivalents"]
        assert self.bs_finprep.short_term_investments == bs_finprep_dict["short_term_investments"]
        assert self.bs_finprep.cash_and_short_term_investments == bs_finprep_dict["cash_and_short_term_investments"]
        assert self.bs_finprep.net_receivables == bs_finprep_dict["net_receivables"]
        assert self.bs_finprep.inventory == bs_finprep_dict["inventory"]
        assert self.bs_finprep.other_current_assets == bs_finprep_dict["other_current_assets"]
        assert self.bs_finprep.total_current_assets == bs_finprep_dict["total_current_assets"]
        assert self.bs_finprep.property_plant_equipment_net == bs_finprep_dict["property_plant_equipment"]
        assert self.bs_finprep.goodwill == bs_finprep_dict["goodwill"]
        assert self.bs_finprep.intangible_assets == bs_finprep_dict["intangible_assets"]
        assert self.bs_finprep.goodwill_and_intangible_assets == bs_finprep_dict["goodwill_and_intangible_assets"]
        assert self.bs_finprep.long_term_investments == bs_finprep_dict["long_term_investments"]
        assert self.bs_finprep.tax_assets == bs_finprep_dict["tax_assets"]
        assert self.bs_finprep.other_non_current_assets == bs_finprep_dict["other_non_current_assets"]
        assert self.bs_finprep.total_non_current_assets == bs_finprep_dict["total_non_current_assets"]
        assert self.bs_finprep.other_assets == bs_finprep_dict["other_assets"]
        assert self.bs_finprep.total_assets == bs_finprep_dict["total_assets"]
        assert self.bs_finprep.account_payables == bs_finprep_dict["account_payables"]
        assert self.bs_finprep.short_term_debt == bs_finprep_dict["short_term_debt"]
        assert self.bs_finprep.tax_payables == bs_finprep_dict["tax_payables"]
        assert self.bs_finprep.deferred_revenue == bs_finprep_dict["deferred_revenue"]
        assert self.bs_finprep.other_current_liabilities == bs_finprep_dict["other_current_liabilities"]
        assert self.bs_finprep.total_current_liabilities == bs_finprep_dict["total_current_liabilities"]
        assert self.bs_finprep.long_term_debt == bs_finprep_dict["long_term_debt"]
        assert self.bs_finprep.deferred_revenue_non_current == bs_finprep_dict["deferred_revenue_non_current"]
        assert (
            self.bs_finprep.deferred_tax_liabilities_non_current
            == bs_finprep_dict["deferred_tax_liabilities_non_current"]
        )
        assert self.bs_finprep.other_non_current_liabilities == bs_finprep_dict["other_non_current_liabilities"]
        assert self.bs_finprep.total_non_current_liabilities == bs_finprep_dict["total_non_current_liabilities"]
        assert self.bs_finprep.other_liabilities == bs_finprep_dict["other_liabilities"]
        assert self.bs_finprep.total_liabilities == bs_finprep_dict["total_liabilities"]
        assert self.bs_finprep.common_stock == bs_finprep_dict["common_stocks"]
        assert self.bs_finprep.retained_earnings == bs_finprep_dict["retained_earnings"]
        assert (
            self.bs_finprep.accumulated_other_comprehensive_income_loss
            == bs_finprep_dict["accumulated_other_comprehensive_income_loss"]
        )
        assert self.bs_finprep.othertotal_stockholders_equity == bs_finprep_dict["othertotal_stockholders_equity"]
        assert self.bs_finprep.total_stockholders_equity == bs_finprep_dict["total_stockholders_equity"]
        assert (
            self.bs_finprep.total_liabilities_and_total_equity == bs_finprep_dict["total_liabilities_and_total_equity"]
        )
        assert self.bs_finprep.total_investments == bs_finprep_dict["total_investments"]
        assert self.bs_finprep.total_debt == bs_finprep_dict["total_debt"]
        assert self.bs_finprep.net_debt == bs_finprep_dict["net_debt"]

    def test_return_standard_cashflow_statement(self):
        cf_st_finprep_dict = self.cf_st_finprep.return_standard
        assert self.cf_st_finprep.net_income == cf_st_finprep_dict["net_income"]
        assert self.cf_st_finprep.depreciation_and_amortization == cf_st_finprep_dict["depreciation_amortization"]
        assert self.cf_st_finprep.deferred_income_tax == cf_st_finprep_dict["deferred_income_tax"]
        assert self.cf_st_finprep.stock_based_compensation == cf_st_finprep_dict["stock_based_compesation"]
        assert self.cf_st_finprep.change_in_working_capital == cf_st_finprep_dict["change_in_working_capital"]
        assert self.cf_st_finprep.accounts_receivables == cf_st_finprep_dict["accounts_receivables"]
        assert self.cf_st_finprep.inventory == cf_st_finprep_dict["inventory"]
        assert self.cf_st_finprep.accounts_payables == cf_st_finprep_dict["accounts_payable"]
        assert self.cf_st_finprep.other_working_capital == cf_st_finprep_dict["other_working_capital"]
        assert self.cf_st_finprep.other_non_cash_items == cf_st_finprep_dict["other_non_cash_items"]
        assert (
            self.cf_st_finprep.net_cash_provided_by_operating_activities
            == cf_st_finprep_dict["operating_activities_cf"]
        )
        assert (
            self.cf_st_finprep.investments_in_property_plant_and_equipment
            == cf_st_finprep_dict["investments_property_plant_equipment"]
        )
        assert self.cf_st_finprep.acquisitions_net == cf_st_finprep_dict["acquisitions_net"]
        assert self.cf_st_finprep.purchases_of_investments == cf_st_finprep_dict["purchases_investments"]
        assert self.cf_st_finprep.sales_maturities_of_investments == cf_st_finprep_dict["sales_maturities_investments"]
        assert self.cf_st_finprep.other_investing_activites == cf_st_finprep_dict["other_investing_activites"]
        assert self.cf_st_finprep.net_cash_used_for_investing_activites == cf_st_finprep_dict["investing_activities_cf"]
        assert self.cf_st_finprep.debt_repayment == cf_st_finprep_dict["debt_repayment"]
        assert self.cf_st_finprep.common_stock_issued == cf_st_finprep_dict["common_stock_issued"]
        assert self.cf_st_finprep.common_stock_repurchased == cf_st_finprep_dict["common_stock_repurchased"]
        assert self.cf_st_finprep.dividends_paid == cf_st_finprep_dict["dividends_paid"]
        assert self.cf_st_finprep.other_financing_activites == cf_st_finprep_dict["other_financing_activities"]
        assert (
            self.cf_st_finprep.net_cash_used_provided_by_financing_activities
            == cf_st_finprep_dict["financing_activities_cf"]
        )
        assert self.cf_st_finprep.effect_of_forex_changes_on_cash == cf_st_finprep_dict["effect_forex_exchange"]
        assert self.cf_st_finprep.net_change_in_cash == cf_st_finprep_dict["net_change_cash"]
        assert self.cf_st_finprep.cash_at_end_of_period == cf_st_finprep_dict["cash_end_period"]
        assert self.cf_st_finprep.cash_at_beginning_of_period == cf_st_finprep_dict["cash_beginning_period"]
        assert self.cf_st_finprep.operating_cash_flow == cf_st_finprep_dict["operating_cf"]
        assert self.cf_st_finprep.capital_expenditure == cf_st_finprep_dict["capex"]
        assert self.cf_st_finprep.free_cash_flow == cf_st_finprep_dict["fcf"]
