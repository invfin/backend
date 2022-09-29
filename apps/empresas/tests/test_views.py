import json

import pytest

from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext

from bfet import DjangoTestingModel as DTM

from rest_framework.test import APITestCase

from apps.api.mixins import BaseAPIViewTest
from apps.general.models import Period
from apps.general.constants import PERIOD_FOR_YEAR
from apps.empresas.models import IncomeStatement, BalanceSheet, CashflowStatement, Company


pytestmark = pytest.mark.django_db

class TestExcelAPIIncome(BaseAPIViewTest, APITestCase):
    path_name = "empresas:ExcelAPIIncome"
    url_path = "/company-information/excel-api/income"
    params = {"ticker": "AAPL"}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(
            IncomeStatement,
            company=DTM.create(Company, name="Apple", ticker="AAPL"),
            period=DTM.create(Period, period=PERIOD_FOR_YEAR),
        )

    # def test_number_of_queries(self):
    #     with CaptureQueriesContext(connection) as ctx:
    #         self.client.get(self.endpoint)
    #     self.assertEqual(len(ctx), 6)

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        self.assertDictEqual(
            json.loads(json.dumps(response.data))[0],
            {
                "date": self.statement.date,
                "reported_currency": self.statement.reported_currency,
                "revenue": self.statement.revenue,
                "cost_of_revenue": self.statement.cost_of_revenue,
                "gross_profit": self.statement.gross_profit,
                "rd_expenses": self.statement.rd_expenses,
                "general_administrative_expenses": self.statement.general_administrative_expenses,
                "selling_marketing_expenses": self.statement.selling_marketing_expenses,
                "sga_expenses": self.statement.sga_expenses,
                "other_expenses": self.statement.other_expenses,
                "operating_expenses": self.statement.operating_expenses,
                "cost_and_expenses": self.statement.cost_and_expenses,
                "interest_expense": self.statement.interest_expense,
                "depreciation_amortization": self.statement.depreciation_amortization,
                "ebitda": self.statement.ebitda,
                "operating_income": self.statement.operating_income,
                "net_total_other_income_expenses": self.statement.net_total_other_income_expenses,
                "income_before_tax": self.statement.income_before_tax,
                "income_tax_expenses": self.statement.income_tax_expenses,
                "net_income": self.statement.net_income,
                "weighted_average_shares_outstanding": self.statement.weighted_average_shares_outstanding,
                "weighted_average_diluated_shares_outstanding": self.statement.weighted_average_diluated_shares_outstanding,
            },
        )


class TestExcelAPIBalance(BaseAPIViewTest, APITestCase):
    path_name = "empresas:ExcelAPIBalance"
    url_path = "/company-information/excel-api/balance"
    params = {"ticker": "AAPL"}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(
            BalanceSheet,
            company=DTM.create(Company, name="Apple", ticker="AAPL"),
            period=DTM.create(Period, period=PERIOD_FOR_YEAR),
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        self.assertDictEqual(
            json.loads(json.dumps(response.data))[0],
            {
                "date": self.statement.date,
                "reported_currency": self.statement.reported_currency,
                "cash_and_cash_equivalents": self.statement.cash_and_cash_equivalents,
                "short_term_investments": self.statement.short_term_investments,
                "cash_and_short_term_investments": self.statement.cash_and_short_term_investments,
                "net_receivables": self.statement.net_receivables,
                "inventory": self.statement.inventory,
                "other_current_assets": self.statement.other_current_assets,
                "total_current_assets": self.statement.total_current_assets,
                "property_plant_equipment": self.statement.property_plant_equipment,
                "goodwill": self.statement.goodwill,
                "intangible_assets": self.statement.intangible_assets,
                "goodwill_and_intangible_assets": self.statement.goodwill_and_intangible_assets,
                "long_term_investments": self.statement.long_term_investments,
                "tax_assets": self.statement.tax_assets,
                "other_non_current_assets": self.statement.other_non_current_assets,
                "total_non_current_assets": self.statement.total_non_current_assets,
                "other_assets": self.statement.other_assets,
                "total_assets": self.statement.total_assets,
                "account_payables": self.statement.account_payables,
                "short_term_debt": self.statement.short_term_debt,
                "tax_payables": self.statement.tax_payables,
                "deferred_revenue": self.statement.deferred_revenue,
                "other_current_liabilities": self.statement.other_current_liabilities,
                "total_current_liabilities": self.statement.total_current_liabilities,
                "long_term_debt": self.statement.long_term_debt,
                "deferred_revenue_non_current": self.statement.deferred_revenue_non_current,
                "deferred_tax_liabilities_non_current": self.statement.deferred_tax_liabilities_non_current,
                "other_non_current_liabilities": self.statement.other_non_current_liabilities,
                "total_non_current_liabilities": self.statement.total_non_current_liabilities,
                "other_liabilities": self.statement.other_liabilities,
                "total_liabilities": self.statement.total_liabilities,
                "common_stocks": self.statement.common_stocks,
                "retained_earnings": self.statement.retained_earnings,
                "accumulated_other_comprehensive_income_loss": self.statement.accumulated_other_comprehensive_income_loss,
                "othertotal_stockholders_equity": self.statement.othertotal_stockholders_equity,
                "total_stockholders_equity": self.statement.total_stockholders_equity,
                "total_liabilities_and_total_equity": self.statement.total_liabilities_and_total_equity,
                "total_investments": self.statement.total_investments,
                "total_debt": self.statement.total_debt,
                "net_debt": self.statement.net_debt,
            },
        )


class TestExcelAPICashflow(BaseAPIViewTest, APITestCase):
    path_name = "empresas:ExcelAPICashflow"
    url_path = "/company-information/excel-api/cashflow"
    params = {"ticker": "AAPL"}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(
            CashflowStatement,
            company=DTM.create(Company, name="Apple", ticker="AAPL"),
            period=DTM.create(Period, period=PERIOD_FOR_YEAR),
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        self.assertDictEqual(
            json.loads(json.dumps(response.data))[0],
            {
                "date": self.statement.date,
                "reported_currency": self.statement.reported_currency,
                "net_income": self.statement.net_income,
                "depreciation_amortization": self.statement.depreciation_amortization,
                "deferred_income_tax": self.statement.deferred_income_tax,
                "stock_based_compesation": self.statement.stock_based_compesation,
                "change_in_working_capital": self.statement.change_in_working_capital,
                "accounts_receivables": self.statement.accounts_receivables,
                "inventory": self.statement.inventory,
                "accounts_payable": self.statement.accounts_payable,
                "other_working_capital": self.statement.other_working_capital,
                "other_non_cash_items": self.statement.other_non_cash_items,
                "operating_activities_cf": self.statement.operating_activities_cf,
                "investments_property_plant_equipment": self.statement.investments_property_plant_equipment,
                "acquisitions_net": self.statement.acquisitions_net,
                "purchases_investments": self.statement.purchases_investments,
                "sales_maturities_investments": self.statement.sales_maturities_investments,
                "other_investing_activites": self.statement.other_investing_activites,
                "investing_activities_cf": self.statement.investing_activities_cf,
                "debt_repayment": self.statement.debt_repayment,
                "common_stock_issued": self.statement.common_stock_issued,
                "common_stock_repurchased": self.statement.common_stock_repurchased,
                "dividends_paid": self.statement.dividends_paid,
                "other_financing_activities": self.statement.other_financing_activities,
                "financing_activities_cf": self.statement.financing_activities_cf,
                "effect_forex_exchange": self.statement.effect_forex_exchange,
                "net_change_cash": self.statement.net_change_cash,
                "cash_end_period": self.statement.cash_end_period,
                "cash_beginning_period": self.statement.cash_beginning_period,
                "operating_cf": self.statement.operating_cf,
                "capex": self.statement.capex,
                "fcf": self.statement.fcf,
            },
        )
