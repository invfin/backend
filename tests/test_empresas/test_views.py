import json

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from bfet import DjangoTestingModel
from rest_framework.test import APITestCase

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.periods import constants
from src.periods.models import Period
from tests.utils import BaseAPIViewTestMixin


class TestExcelAPIIncome(BaseAPIViewTestMixin, APITestCase):
    path_name = "empresas:ExcelAPIIncome"
    url_path = "/company-information/excel-api/income"
    params = {"ticker": "INTC"}
    actual_api = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.clean_company = DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        cls.period_for_year = DjangoTestingModel.create(Period, year=2022, period=constants.PERIOD_FOR_YEAR)
        cls.yearly_income_statement = DjangoTestingModel.create(
            IncomeStatement, is_ttm=False, company=cls.clean_company, period=cls.period_for_year
        )

    # def test_number_of_queries(self):
    #     with CaptureQueriesContext(connection) as ctx:
    #         self.self.client.get(self.endpoint)
    #     assert(len(ctx), 6)

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": self.yearly_income_statement.date,
            "reported_currency": self.yearly_income_statement.reported_currency,
            "revenue": self.yearly_income_statement.revenue,
            "cost_of_revenue": self.yearly_income_statement.cost_of_revenue,
            "gross_profit": self.yearly_income_statement.gross_profit,
            "rd_expenses": self.yearly_income_statement.rd_expenses,
            "general_administrative_expenses": self.yearly_income_statement.general_administrative_expenses,
            "selling_marketing_expenses": self.yearly_income_statement.selling_marketing_expenses,
            "sga_expenses": self.yearly_income_statement.sga_expenses,
            "other_expenses": self.yearly_income_statement.other_expenses,
            "operating_expenses": self.yearly_income_statement.operating_expenses,
            "cost_and_expenses": self.yearly_income_statement.cost_and_expenses,
            "interest_expense": self.yearly_income_statement.interest_expense,
            "depreciation_amortization": self.yearly_income_statement.depreciation_amortization,
            "ebitda": self.yearly_income_statement.ebitda,
            "operating_income": self.yearly_income_statement.operating_income,
            "net_total_other_income_expenses": self.yearly_income_statement.net_total_other_income_expenses,
            "income_before_tax": self.yearly_income_statement.income_before_tax,
            "income_tax_expenses": self.yearly_income_statement.income_tax_expenses,
            "net_income": self.yearly_income_statement.net_income,
            "weighted_average_shares_outstanding": self.yearly_income_statement.weighted_average_shares_outstanding,
            "weighted_average_diluated_shares_outstanding": self.yearly_income_statement.weighted_average_diluated_shares_outstanding,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data


class TestExcelAPIBalance(BaseAPIViewTestMixin, APITestCase):
    path_name = "empresas:ExcelAPIBalance"
    url_path = "/company-information/excel-api/balance"
    params = {"ticker": "INTC"}
    actual_api = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.clean_company = DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        cls.period_for_year = DjangoTestingModel.create(Period, year=2022, period=constants.PERIOD_FOR_YEAR)
        cls.yearly_balance_sheet = DjangoTestingModel.create(
            BalanceSheet, is_ttm=False, company=cls.clean_company, period=cls.period_for_year
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": self.yearly_balance_sheet.date,
            "reported_currency": self.yearly_balance_sheet.reported_currency,
            "cash_and_cash_equivalents": self.yearly_balance_sheet.cash_and_cash_equivalents,
            "short_term_investments": self.yearly_balance_sheet.short_term_investments,
            "cash_and_short_term_investments": self.yearly_balance_sheet.cash_and_short_term_investments,
            "net_receivables": self.yearly_balance_sheet.net_receivables,
            "inventory": self.yearly_balance_sheet.inventory,
            "other_current_assets": self.yearly_balance_sheet.other_current_assets,
            "total_current_assets": self.yearly_balance_sheet.total_current_assets,
            "property_plant_equipment": self.yearly_balance_sheet.property_plant_equipment,
            "goodwill": self.yearly_balance_sheet.goodwill,
            "intangible_assets": self.yearly_balance_sheet.intangible_assets,
            "goodwill_and_intangible_assets": self.yearly_balance_sheet.goodwill_and_intangible_assets,
            "long_term_investments": self.yearly_balance_sheet.long_term_investments,
            "tax_assets": self.yearly_balance_sheet.tax_assets,
            "other_non_current_assets": self.yearly_balance_sheet.other_non_current_assets,
            "total_non_current_assets": self.yearly_balance_sheet.total_non_current_assets,
            "other_assets": self.yearly_balance_sheet.other_assets,
            "total_assets": self.yearly_balance_sheet.total_assets,
            "accounts_payable": self.yearly_balance_sheet.accounts_payable,
            "short_term_debt": self.yearly_balance_sheet.short_term_debt,
            "tax_payables": self.yearly_balance_sheet.tax_payables,
            "deferred_revenue": self.yearly_balance_sheet.deferred_revenue,
            "other_current_liabilities": self.yearly_balance_sheet.other_current_liabilities,
            "total_current_liabilities": self.yearly_balance_sheet.total_current_liabilities,
            "long_term_debt": self.yearly_balance_sheet.long_term_debt,
            "deferred_revenue_non_current": self.yearly_balance_sheet.deferred_revenue_non_current,
            "deferred_tax_liabilities_non_current": self.yearly_balance_sheet.deferred_tax_liabilities_non_current,
            "other_non_current_liabilities": self.yearly_balance_sheet.other_non_current_liabilities,
            "total_non_current_liabilities": self.yearly_balance_sheet.total_non_current_liabilities,
            "other_liabilities": self.yearly_balance_sheet.other_liabilities,
            "total_liabilities": self.yearly_balance_sheet.total_liabilities,
            "common_stocks": self.yearly_balance_sheet.common_stocks,
            "retained_earnings": self.yearly_balance_sheet.retained_earnings,
            "accumulated_other_comprehensive_income_loss": self.yearly_balance_sheet.accumulated_other_comprehensive_income_loss,
            "othertotal_stockholders_equity": self.yearly_balance_sheet.othertotal_stockholders_equity,
            "total_stockholders_equity": self.yearly_balance_sheet.total_stockholders_equity,
            "total_liabilities_and_total_equity": self.yearly_balance_sheet.total_liabilities_and_total_equity,
            "total_investments": self.yearly_balance_sheet.total_investments,
            "total_debt": self.yearly_balance_sheet.total_debt,
            "net_debt": self.yearly_balance_sheet.net_debt,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data


class TestExcelAPICashflow(BaseAPIViewTestMixin, APITestCase):
    path_name = "empresas:ExcelAPICashflow"
    url_path = "/company-information/excel-api/cashflow"
    params = {"ticker": "INTC"}
    actual_api = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.clean_company = DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        cls.period_for_year = DjangoTestingModel.create(Period, year=2022, period=constants.PERIOD_FOR_YEAR)
        cls.yearly_cashflow_statement = DjangoTestingModel.create(
            CashflowStatement, is_ttm=False, company=cls.clean_company, period=cls.period_for_year
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = {
            "date": self.yearly_cashflow_statement.date,
            "reported_currency": self.yearly_cashflow_statement.reported_currency,
            "net_income": self.yearly_cashflow_statement.net_income,
            "depreciation_amortization": self.yearly_cashflow_statement.depreciation_amortization,
            "deferred_income_tax": self.yearly_cashflow_statement.deferred_income_tax,
            "stock_based_compensation": self.yearly_cashflow_statement.stock_based_compensation,
            "change_in_working_capital": self.yearly_cashflow_statement.change_in_working_capital,
            "accounts_receivable": self.yearly_cashflow_statement.accounts_receivable,
            "inventory": self.yearly_cashflow_statement.inventory,
            "accounts_payable": self.yearly_cashflow_statement.accounts_payable,
            "other_working_capital": self.yearly_cashflow_statement.other_working_capital,
            "other_non_cash_items": self.yearly_cashflow_statement.other_non_cash_items,
            "operating_activities_cf": self.yearly_cashflow_statement.operating_activities_cf,
            "investments_property_plant_equipment": self.yearly_cashflow_statement.investments_property_plant_equipment,
            "acquisitions_net": self.yearly_cashflow_statement.acquisitions_net,
            "purchases_investments": self.yearly_cashflow_statement.purchases_investments,
            "sales_maturities_investments": self.yearly_cashflow_statement.sales_maturities_investments,
            "other_investing_activites": self.yearly_cashflow_statement.other_investing_activites,
            "investing_activities_cf": self.yearly_cashflow_statement.investing_activities_cf,
            "debt_repayment": self.yearly_cashflow_statement.debt_repayment,
            "common_stock_issued": self.yearly_cashflow_statement.common_stock_issued,
            "common_stock_repurchased": self.yearly_cashflow_statement.common_stock_repurchased,
            "dividends_paid": self.yearly_cashflow_statement.dividends_paid,
            "other_financing_activities": self.yearly_cashflow_statement.other_financing_activities,
            "financing_activities_cf": self.yearly_cashflow_statement.financing_activities_cf,
            "effect_forex_exchange": self.yearly_cashflow_statement.effect_forex_exchange,
            "net_change_cash": self.yearly_cashflow_statement.net_change_cash,
            "cash_end_period": self.yearly_cashflow_statement.cash_end_period,
            "cash_beginning_period": self.yearly_cashflow_statement.cash_beginning_period,
            "operating_cf": self.yearly_cashflow_statement.operating_cf,
            "capex": self.yearly_cashflow_statement.capex,
            "fcf": self.yearly_cashflow_statement.fcf,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data
