import json
from unittest.mock import MagicMock

from django.test import TestCase

from bfet import DjangoTestingModel
from rest_framework.test import APITestCase

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.views import Suggestor
from src.periods import constants
from src.periods.models import Period
from tests.utils import BaseAPIViewTestMixin


class TestSuggestor(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            name="Apple",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        )
        DjangoTestingModel.create(
            Company,
            ticker="INTC",
            name="Intel",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        )
        DjangoTestingModel.create(
            Company,
            ticker="BABA",
            name="Alibaba",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        )

    def test_suggest_companies(self):
        self.assertEqual(Suggestor.suggest_companies("AAPL"), ["Apple [AAPL]"])

    def test_companies_searcher(self):
        result = Suggestor.companies_searcher(MagicMock(GET={"term": "AAPL"}))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), ["Apple [AAPL]"])
        self.assertEqual(result.headers, {"Content-Type": "application/json"})


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
        cls.period_for_year = DjangoTestingModel.create(
            Period,
            year=2022,
            period=constants.PERIOD_FOR_YEAR,
        )
        cls.yearly_income_statement = DjangoTestingModel.create(
            IncomeStatement,
            is_ttm=False,
            company=cls.clean_company,
            period=cls.period_for_year,
        )

    # def test_number_of_queries(self):
    #     with CaptureQueriesContext(connection) as ctx:
    #         self.self.client.get(self.endpoint)
    #     assert(len(ctx), 6)

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        yis = self.yearly_income_statement
        expected_data = {
            "date": yis.date,
            "reported_currency": yis.reported_currency,
            "revenue": yis.revenue,
            "cost_of_revenue": yis.cost_of_revenue,
            "gross_profit": yis.gross_profit,
            "rd_expenses": yis.rd_expenses,
            "general_administrative_expenses": yis.general_administrative_expenses,
            "selling_marketing_expenses": yis.selling_marketing_expenses,
            "sga_expenses": yis.sga_expenses,
            "other_expenses": yis.other_expenses,
            "operating_expenses": yis.operating_expenses,
            "cost_and_expenses": yis.cost_and_expenses,
            "interest_expense": yis.interest_expense,
            "depreciation_amortization": yis.depreciation_amortization,
            "ebitda": yis.ebitda,
            "operating_income": yis.operating_income,
            "net_total_other_income_expenses": yis.net_total_other_income_expenses,
            "income_before_tax": yis.income_before_tax,
            "income_tax_expenses": yis.income_tax_expenses,
            "net_income": yis.net_income,
            "weighted_average_shares_outstanding": yis.weighted_average_shares_outstanding,
            "weighted_average_diluated_shares_outstanding": (
                yis.weighted_average_diluated_shares_outstanding
            ),
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
        cls.period_for_year = DjangoTestingModel.create(
            Period,
            year=2022,
            period=constants.PERIOD_FOR_YEAR,
        )
        cls.yearly_balance_sheet = DjangoTestingModel.create(
            BalanceSheet,
            is_ttm=False,
            company=cls.clean_company,
            period=cls.period_for_year,
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        ybs = self.yearly_balance_sheet
        expected_data = {
            "date": ybs.date,
            "reported_currency": ybs.reported_currency,
            "cash_and_cash_equivalents": ybs.cash_and_cash_equivalents,
            "short_term_investments": ybs.short_term_investments,
            "cash_and_short_term_investments": ybs.cash_and_short_term_investments,
            "net_receivables": ybs.net_receivables,
            "inventory": ybs.inventory,
            "other_current_assets": ybs.other_current_assets,
            "total_current_assets": ybs.total_current_assets,
            "property_plant_equipment": ybs.property_plant_equipment,
            "goodwill": ybs.goodwill,
            "intangible_assets": ybs.intangible_assets,
            "goodwill_and_intangible_assets": ybs.goodwill_and_intangible_assets,
            "long_term_investments": ybs.long_term_investments,
            "tax_assets": ybs.tax_assets,
            "other_non_current_assets": ybs.other_non_current_assets,
            "total_non_current_assets": ybs.total_non_current_assets,
            "other_assets": ybs.other_assets,
            "total_assets": ybs.total_assets,
            "accounts_payable": ybs.accounts_payable,
            "short_term_debt": ybs.short_term_debt,
            "tax_payables": ybs.tax_payables,
            "deferred_revenue": ybs.deferred_revenue,
            "other_current_liabilities": ybs.other_current_liabilities,
            "total_current_liabilities": ybs.total_current_liabilities,
            "long_term_debt": ybs.long_term_debt,
            "deferred_revenue_non_current": ybs.deferred_revenue_non_current,
            "deferred_tax_liabilities_non_current": ybs.deferred_tax_liabilities_non_current,
            "other_non_current_liabilities": ybs.other_non_current_liabilities,
            "total_non_current_liabilities": ybs.total_non_current_liabilities,
            "other_liabilities": ybs.other_liabilities,
            "total_liabilities": ybs.total_liabilities,
            "common_stocks": ybs.common_stocks,
            "retained_earnings": ybs.retained_earnings,
            "accumulated_other_comprehensive_income_loss": (
                ybs.accumulated_other_comprehensive_income_loss
            ),
            "othertotal_stockholders_equity": ybs.othertotal_stockholders_equity,
            "total_stockholders_equity": ybs.total_stockholders_equity,
            "total_liabilities_and_total_equity": ybs.total_liabilities_and_total_equity,
            "total_investments": ybs.total_investments,
            "total_debt": ybs.total_debt,
            "net_debt": ybs.net_debt,
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
        cls.period_for_year = DjangoTestingModel.create(
            Period,
            year=2022,
            period=constants.PERIOD_FOR_YEAR,
        )
        cls.yearly_cashflow_statement = DjangoTestingModel.create(
            CashflowStatement,
            is_ttm=False,
            company=cls.clean_company,
            period=cls.period_for_year,
        )

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        ycs = self.yearly_cashflow_statement
        expected_data = {
            "date": ycs.date,
            "reported_currency": ycs.reported_currency,
            "net_income": ycs.net_income,
            "depreciation_amortization": ycs.depreciation_amortization,
            "deferred_income_tax": ycs.deferred_income_tax,
            "stock_based_compensation": ycs.stock_based_compensation,
            "change_in_working_capital": ycs.change_in_working_capital,
            "accounts_receivable": ycs.accounts_receivable,
            "inventory": ycs.inventory,
            "accounts_payable": ycs.accounts_payable,
            "other_working_capital": ycs.other_working_capital,
            "other_non_cash_items": ycs.other_non_cash_items,
            "operating_activities_cf": ycs.operating_activities_cf,
            "investments_property_plant_equipment": ycs.investments_property_plant_equipment,
            "acquisitions_net": ycs.acquisitions_net,
            "purchases_investments": ycs.purchases_investments,
            "sales_maturities_investments": ycs.sales_maturities_investments,
            "other_investing_activites": ycs.other_investing_activites,
            "investing_activities_cf": ycs.investing_activities_cf,
            "debt_repayment": ycs.debt_repayment,
            "common_stock_issued": ycs.common_stock_issued,
            "common_stock_repurchased": ycs.common_stock_repurchased,
            "dividends_paid": ycs.dividends_paid,
            "other_financing_activities": ycs.other_financing_activities,
            "financing_activities_cf": ycs.financing_activities_cf,
            "effect_forex_exchange": ycs.effect_forex_exchange,
            "net_change_cash": ycs.net_change_cash,
            "cash_end_period": ycs.cash_end_period,
            "cash_beginning_period": ycs.cash_beginning_period,
            "operating_cf": ycs.operating_cf,
            "capex": ycs.capex,
            "fcf": ycs.fcf,
        }
        assert json.loads(json.dumps(response.data))[0] == expected_data
