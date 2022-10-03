import json
import pytest

from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext

from apps.api.mixins import BaseAPIViewTest


@pytest.mark.django_db
class TestExcelAPIIncome(BaseAPIViewTest):
    path_name = "empresas:ExcelAPIIncome"
    url_path = "/company-information/excel-api/income"
    params = {"ticker": "INTC"}

    # def test_number_of_queries(self):
    #     with CaptureQueriesContext(connection) as ctx:
    #         self.client.get(self.endpoint)
    #     assert(len(ctx), 6)

    def test_success_response(self, client, yearly_income_statement):
        response = client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": yearly_income_statement.date,
            "reported_currency": yearly_income_statement.reported_currency,
            "revenue": yearly_income_statement.revenue,
            "cost_of_revenue": yearly_income_statement.cost_of_revenue,
            "gross_profit": yearly_income_statement.gross_profit,
            "rd_expenses": yearly_income_statement.rd_expenses,
            "general_administrative_expenses": yearly_income_statement.general_administrative_expenses,
            "selling_marketing_expenses": yearly_income_statement.selling_marketing_expenses,
            "sga_expenses": yearly_income_statement.sga_expenses,
            "other_expenses": yearly_income_statement.other_expenses,
            "operating_expenses": yearly_income_statement.operating_expenses,
            "cost_and_expenses": yearly_income_statement.cost_and_expenses,
            "interest_expense": yearly_income_statement.interest_expense,
            "depreciation_amortization": yearly_income_statement.depreciation_amortization,
            "ebitda": yearly_income_statement.ebitda,
            "operating_income": yearly_income_statement.operating_income,
            "net_total_other_income_expenses": yearly_income_statement.net_total_other_income_expenses,
            "income_before_tax": yearly_income_statement.income_before_tax,
            "income_tax_expenses": yearly_income_statement.income_tax_expenses,
            "net_income": yearly_income_statement.net_income,
            "weighted_average_shares_outstanding": yearly_income_statement.weighted_average_shares_outstanding,
            "weighted_average_diluated_shares_outstanding": yearly_income_statement.weighted_average_diluated_shares_outstanding,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data


@pytest.mark.django_db
class TestExcelAPIBalance(BaseAPIViewTest):
    path_name = "empresas:ExcelAPIBalance"
    url_path = "/company-information/excel-api/balance"
    params = {"ticker": "INTC"}

    def test_success_response(self, client, yearly_balance_sheet):
        response = client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": yearly_balance_sheet.date,
            "reported_currency": yearly_balance_sheet.reported_currency,
            "cash_and_cash_equivalents": yearly_balance_sheet.cash_and_cash_equivalents,
            "short_term_investments": yearly_balance_sheet.short_term_investments,
            "cash_and_short_term_investments": yearly_balance_sheet.cash_and_short_term_investments,
            "net_receivables": yearly_balance_sheet.net_receivables,
            "inventory": yearly_balance_sheet.inventory,
            "other_current_assets": yearly_balance_sheet.other_current_assets,
            "total_current_assets": yearly_balance_sheet.total_current_assets,
            "property_plant_equipment": yearly_balance_sheet.property_plant_equipment,
            "goodwill": yearly_balance_sheet.goodwill,
            "intangible_assets": yearly_balance_sheet.intangible_assets,
            "goodwill_and_intangible_assets": yearly_balance_sheet.goodwill_and_intangible_assets,
            "long_term_investments": yearly_balance_sheet.long_term_investments,
            "tax_assets": yearly_balance_sheet.tax_assets,
            "other_non_current_assets": yearly_balance_sheet.other_non_current_assets,
            "total_non_current_assets": yearly_balance_sheet.total_non_current_assets,
            "other_assets": yearly_balance_sheet.other_assets,
            "total_assets": yearly_balance_sheet.total_assets,
            "account_payables": yearly_balance_sheet.account_payables,
            "short_term_debt": yearly_balance_sheet.short_term_debt,
            "tax_payables": yearly_balance_sheet.tax_payables,
            "deferred_revenue": yearly_balance_sheet.deferred_revenue,
            "other_current_liabilities": yearly_balance_sheet.other_current_liabilities,
            "total_current_liabilities": yearly_balance_sheet.total_current_liabilities,
            "long_term_debt": yearly_balance_sheet.long_term_debt,
            "deferred_revenue_non_current": yearly_balance_sheet.deferred_revenue_non_current,
            "deferred_tax_liabilities_non_current": yearly_balance_sheet.deferred_tax_liabilities_non_current,
            "other_non_current_liabilities": yearly_balance_sheet.other_non_current_liabilities,
            "total_non_current_liabilities": yearly_balance_sheet.total_non_current_liabilities,
            "other_liabilities": yearly_balance_sheet.other_liabilities,
            "total_liabilities": yearly_balance_sheet.total_liabilities,
            "common_stocks": yearly_balance_sheet.common_stocks,
            "retained_earnings": yearly_balance_sheet.retained_earnings,
            "accumulated_other_comprehensive_income_loss": yearly_balance_sheet.accumulated_other_comprehensive_income_loss,
            "othertotal_stockholders_equity": yearly_balance_sheet.othertotal_stockholders_equity,
            "total_stockholders_equity": yearly_balance_sheet.total_stockholders_equity,
            "total_liabilities_and_total_equity": yearly_balance_sheet.total_liabilities_and_total_equity,
            "total_investments": yearly_balance_sheet.total_investments,
            "total_debt": yearly_balance_sheet.total_debt,
            "net_debt": yearly_balance_sheet.net_debt,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data


@pytest.mark.django_db
class TestExcelAPICashflow(BaseAPIViewTest):
    path_name = "empresas:ExcelAPICashflow"
    url_path = "/company-information/excel-api/cashflow"
    params = {"ticker": "INTC"}

    def test_success_response(self, client, yearly_cashflow_statement):
        response = client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": yearly_cashflow_statement.date,
            "reported_currency": yearly_cashflow_statement.reported_currency,
            "net_income": yearly_cashflow_statement.net_income,
            "depreciation_amortization": yearly_cashflow_statement.depreciation_amortization,
            "deferred_income_tax": yearly_cashflow_statement.deferred_income_tax,
            "stock_based_compesation": yearly_cashflow_statement.stock_based_compesation,
            "change_in_working_capital": yearly_cashflow_statement.change_in_working_capital,
            "accounts_receivables": yearly_cashflow_statement.accounts_receivables,
            "inventory": yearly_cashflow_statement.inventory,
            "accounts_payable": yearly_cashflow_statement.accounts_payable,
            "other_working_capital": yearly_cashflow_statement.other_working_capital,
            "other_non_cash_items": yearly_cashflow_statement.other_non_cash_items,
            "operating_activities_cf": yearly_cashflow_statement.operating_activities_cf,
            "investments_property_plant_equipment": yearly_cashflow_statement.investments_property_plant_equipment,
            "acquisitions_net": yearly_cashflow_statement.acquisitions_net,
            "purchases_investments": yearly_cashflow_statement.purchases_investments,
            "sales_maturities_investments": yearly_cashflow_statement.sales_maturities_investments,
            "other_investing_activites": yearly_cashflow_statement.other_investing_activites,
            "investing_activities_cf": yearly_cashflow_statement.investing_activities_cf,
            "debt_repayment": yearly_cashflow_statement.debt_repayment,
            "common_stock_issued": yearly_cashflow_statement.common_stock_issued,
            "common_stock_repurchased": yearly_cashflow_statement.common_stock_repurchased,
            "dividends_paid": yearly_cashflow_statement.dividends_paid,
            "other_financing_activities": yearly_cashflow_statement.other_financing_activities,
            "financing_activities_cf": yearly_cashflow_statement.financing_activities_cf,
            "effect_forex_exchange": yearly_cashflow_statement.effect_forex_exchange,
            "net_change_cash": yearly_cashflow_statement.net_change_cash,
            "cash_end_period": yearly_cashflow_statement.cash_end_period,
            "cash_beginning_period": yearly_cashflow_statement.cash_beginning_period,
            "operating_cf": yearly_cashflow_statement.operating_cf,
            "capex": yearly_cashflow_statement.capex,
            "fcf": yearly_cashflow_statement.fcf,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data
