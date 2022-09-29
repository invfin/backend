import vcr

from bfet import DjangoTestingModel as DTM

import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db

from apps.empresas.models import (
    BalanceSheetFinprep,
    IncomeStatementFinprep,
    CashflowStatementFinprep,
    Company
)
from apps.empresas.parse.finprep import FinprepInfo
from apps.empresas.parse.finprep.normalize_data import NormalizeFinprep
from apps.empresas.parse.finprep.parse_data import ParseFinprep
from apps.empresas.tests import finprep_data


parse_vcr = vcr.VCR(
    cassette_library_dir='cassettes/company/parse/finprep/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_income_statements_finprep(self):
        comp_data = self.parser.request_income_statements_finprep("AAPL")
        self.assertEqual(finprep_data.INCOME_STATEMENT, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_balance_sheets_finprep(self):
        comp_data = self.parser.request_balance_sheets_finprep("AAPL")
        self.assertEqual(finprep_data.BALANCE_SHEET, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_cashflow_statements_finprep(self):
        comp_data = self.parser.request_cashflow_statements_finprep("AAPL")
        self.assertEqual(finprep_data.CASHFLOW_STATEMENT, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_financials_finprep(self):
        comp_data = self.parser.request_financials_finprep("AAPL")
        self.assertEqual(finprep_data.DICT_STATEMENTS, comp_data)


class TestNormalizeFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = NormalizeFinprep()
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser.company = cls.company
        cls.income_statement = finprep_data.INCOME_STATEMENT[0]
        cls.balance_sheet = finprep_data.BALANCE_SHEET[0]
        cls.cashflow_statement = finprep_data.CASHFLOW_STATEMENT[0]

    def test_normalize_income_statements_finprep(self):
        comp_data = self.parser.normalize_income_statements_finprep(self.income_statement)
        self.assertTrue("accepted_date" in comp_data)
        self.assertTrue("filling_date" in comp_data)
        self.assertTrue("final_link" in comp_data)
        self.assertTrue("link" in comp_data)
        self.assertTrue("reported_currency" in comp_data)
        self.assertTrue("calendar_year" in comp_data)
        self.assertTrue("cik" in comp_data)
        self.assertTrue("symbol" in comp_data)
        self.assertTrue("cost_and_expenses" in comp_data)
        self.assertTrue("cost_of_revenue" in comp_data)
        self.assertTrue("depreciation_and_amortization" in comp_data)
        self.assertTrue("ebitda" in comp_data)
        self.assertTrue("ebitdaratio" in comp_data)
        self.assertTrue("eps" in comp_data)
        self.assertTrue("epsdiluted" in comp_data)
        self.assertTrue("general_and_administrative_expenses" in comp_data)
        self.assertTrue("gross_profit" in comp_data)
        self.assertTrue("gross_profit_ratio" in comp_data)
        self.assertTrue("income_before_tax" in comp_data)
        self.assertTrue("income_before_tax_ratio" in comp_data)
        self.assertTrue("income_tax_expense" in comp_data)
        self.assertTrue("interest_expense" in comp_data)
        self.assertTrue("interest_income" in comp_data)
        self.assertTrue("net_income" in comp_data)
        self.assertTrue("net_income_ratio" in comp_data)
        self.assertTrue("operating_expenses" in comp_data)
        self.assertTrue("operating_income" in comp_data)
        self.assertTrue("operating_income_ratio" in comp_data)
        self.assertTrue("other_expenses" in comp_data)
        self.assertTrue("research_and_development_expenses" in comp_data)
        self.assertTrue("revenue" in comp_data)
        self.assertTrue("selling_and_marketing_expenses" in comp_data)
        self.assertTrue("selling_general_and_administrative_expenses" in comp_data)
        self.assertTrue("total_other_income_expenses_net" in comp_data)
        self.assertTrue("weighted_average_shs_out" in comp_data)
        self.assertTrue("weighted_average_shs_out_dil" in comp_data)

    def test_normalize_balance_sheets_finprep(self):
        comp_data = self.parser.normalize_balance_sheets_finprep(self.balance_sheet)
        self.assertTrue("accepted_date" in comp_data)
        self.assertTrue("filling_date" in comp_data)
        self.assertTrue("final_link" in comp_data)
        self.assertTrue("link" in comp_data)
        self.assertTrue("reported_currency" in comp_data)
        self.assertTrue("calendar_year" in comp_data)
        self.assertTrue("cik" in comp_data)
        self.assertTrue("symbol" in comp_data)
        self.assertTrue("account_payables" in comp_data)
        self.assertTrue("accumulated_other_comprehensive_income_loss" in comp_data)
        self.assertTrue("capital_lease_obligations" in comp_data)
        self.assertTrue("cash_and_cash_equivalents" in comp_data)
        self.assertTrue("cash_and_short_term_investments" in comp_data)
        self.assertTrue("common_stock" in comp_data)
        self.assertTrue("deferred_revenue" in comp_data)
        self.assertTrue("deferred_revenue_non_current" in comp_data)
        self.assertTrue("deferred_tax_liabilities_non_current" in comp_data)
        self.assertTrue("goodwill" in comp_data)
        self.assertTrue("goodwill_and_intangible_assets" in comp_data)
        self.assertTrue("intangible_assets" in comp_data)
        self.assertTrue("inventory" in comp_data)
        self.assertTrue("long_term_debt" in comp_data)
        self.assertTrue("long_term_investments" in comp_data)
        self.assertTrue("minority_interest" in comp_data)
        self.assertTrue("net_debt" in comp_data)
        self.assertTrue("net_receivables" in comp_data)
        self.assertTrue("other_assets" in comp_data)
        self.assertTrue("other_current_assets" in comp_data)
        self.assertTrue("other_current_liabilities" in comp_data)
        self.assertTrue("other_liabilities" in comp_data)
        self.assertTrue("other_non_current_assets" in comp_data)
        self.assertTrue("other_non_current_liabilities" in comp_data)
        self.assertTrue("othertotal_stockholders_equity" in comp_data)
        self.assertTrue("preferred_stock" in comp_data)
        self.assertTrue("property_plant_equipment_net" in comp_data)
        self.assertTrue("retained_earnings" in comp_data)
        self.assertTrue("short_term_debt" in comp_data)
        self.assertTrue("short_term_investments" in comp_data)
        self.assertTrue("tax_assets" in comp_data)
        self.assertTrue("tax_payables" in comp_data)
        self.assertTrue("total_assets" in comp_data)
        self.assertTrue("total_current_assets" in comp_data)
        self.assertTrue("total_current_liabilities" in comp_data)
        self.assertTrue("total_debt" in comp_data)
        self.assertTrue("total_equity" in comp_data)
        self.assertTrue("total_investments" in comp_data)
        self.assertTrue("total_liabilities" in comp_data)
        self.assertTrue("total_liabilities_and_stockholders_equity" in comp_data)
        self.assertTrue("total_liabilities_and_total_equity" in comp_data)
        self.assertTrue("total_non_current_assets" in comp_data)
        self.assertTrue("total_non_current_liabilities" in comp_data)
        self.assertTrue("total_stockholders_equity" in comp_data)

    def test_normalize_cashflow_statements_finprep(self):
        comp_data = self.parser.normalize_cashflow_statements_finprep(self.cashflow_statement)
        self.assertTrue("accepted_date" in comp_data)
        self.assertTrue("filling_date" in comp_data)
        self.assertTrue("final_link" in comp_data)
        self.assertTrue("link" in comp_data)
        self.assertTrue("reported_currency" in comp_data)
        self.assertTrue("calendar_year" in comp_data)
        self.assertTrue("cik" in comp_data)
        self.assertTrue("symbol" in comp_data)
        self.assertTrue("accounts_payables" in comp_data)
        self.assertTrue("accounts_receivables" in comp_data)
        self.assertTrue("acquisitions_net" in comp_data)
        self.assertTrue("capital_expenditure" in comp_data)
        self.assertTrue("cash_at_beginning_of_period" in comp_data)
        self.assertTrue("cash_at_end_of_period" in comp_data)
        self.assertTrue("change_in_working_capital" in comp_data)
        self.assertTrue("common_stock_issued" in comp_data)
        self.assertTrue("common_stock_repurchased" in comp_data)
        self.assertTrue("debt_repayment" in comp_data)
        self.assertTrue("deferred_income_tax" in comp_data)
        self.assertTrue("depreciation_and_amortization" in comp_data)
        self.assertTrue("dividends_paid" in comp_data)
        self.assertTrue("effect_of_forex_changes_on_cash" in comp_data)
        self.assertTrue("free_cash_flow" in comp_data)
        self.assertTrue("inventory" in comp_data)
        self.assertTrue("investments_in_property_plant_and_equipment" in comp_data)
        self.assertTrue("net_cash_provided_by_operating_activities" in comp_data)
        self.assertTrue("net_cash_used_for_investing_activites" in comp_data)
        self.assertTrue("net_cash_used_provided_by_financing_activities" in comp_data)
        self.assertTrue("net_change_in_cash" in comp_data)
        self.assertTrue("net_income" in comp_data)
        self.assertTrue("operating_cash_flow" in comp_data)
        self.assertTrue("other_financing_activites" in comp_data)
        self.assertTrue("other_investing_activites" in comp_data)
        self.assertTrue("other_non_cash_items" in comp_data)
        self.assertTrue("other_working_capital" in comp_data)
        self.assertTrue("purchases_of_investments" in comp_data)
        self.assertTrue("sales_maturities_of_investments" in comp_data)
        self.assertTrue("stock_based_compensation" in comp_data)

class TestFinprepInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser = FinprepInfo(cls.company)
        cls.normalizer = NormalizeFinprep()

    @parse_vcr.use_cassette("test_request_income_statements_finprep", filter_query_parameters=['apikey'])
    def test_create_income_statements_finprep(self):
        self.assertEqual(0, IncomeStatementFinprep.objects.all().count())
        self.parser.create_income_statements_finprep()
        self.assertEqual(5, IncomeStatementFinprep.objects.all().count())
        old_number_statements_created = IncomeStatementFinprep.objects.all().count()
        previous_list_data = [statement for statement in IncomeStatementFinprep.objects.all()]
        IncomeStatementFinprep.objects.all().delete()
        self.assertEqual(0, IncomeStatementFinprep.objects.all().count())
        for statement in finprep_data.INCOME_STATEMENT:
            IncomeStatementFinprep.objects.create(
                **self.normalizer.normalize_income_statements_finprep(statement)
            )
        self.assertEqual(5, IncomeStatementFinprep.objects.all().count())
        self.assertEqual(old_number_statements_created, IncomeStatementFinprep.objects.all().count())
        for statement in previous_list_data:
            new_statement = IncomeStatementFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                self.assertEqual(statement.accepted_date, new_statement.accepted_date)
                self.assertEqual(statement.filling_date, new_statement.filling_date)
                self.assertEqual(statement.final_link, new_statement.final_link)
                self.assertEqual(statement.link, new_statement.link)
                self.assertEqual(statement.reported_currency, new_statement.reported_currency)
                self.assertEqual(statement.calendar_year, new_statement.calendar_year)
                self.assertEqual(statement.cik, new_statement.cik)
                self.assertEqual(statement.symbol, new_statement.symbol)
                self.assertEqual(statement.cost_and_expenses, new_statement.cost_and_expenses)
                self.assertEqual(statement.cost_of_revenue, new_statement.cost_of_revenue)
                self.assertEqual(statement.depreciation_and_amortization, new_statement.depreciation_and_amortization)
                self.assertEqual(statement.ebitda, new_statement.ebitda)
                self.assertEqual(statement.ebitdaratio, new_statement.ebitdaratio)
                self.assertEqual(statement.eps, new_statement.eps)
                self.assertEqual(statement.epsdiluted, new_statement.epsdiluted)
                self.assertEqual(statement.general_and_administrative_expenses, new_statement.general_and_administrative_expenses)
                self.assertEqual(statement.gross_profit, new_statement.gross_profit)
                self.assertEqual(statement.gross_profit_ratio, new_statement.gross_profit_ratio)
                self.assertEqual(statement.income_before_tax, new_statement.income_before_tax)
                self.assertEqual(statement.income_before_tax_ratio, new_statement.income_before_tax_ratio)
                self.assertEqual(statement.income_tax_expense, new_statement.income_tax_expense)
                self.assertEqual(statement.interest_expense, new_statement.interest_expense)
                self.assertEqual(statement.interest_income, new_statement.interest_income)
                self.assertEqual(statement.net_income, new_statement.net_income)
                self.assertEqual(statement.net_income_ratio, new_statement.net_income_ratio)
                self.assertEqual(statement.operating_expenses, new_statement.operating_expenses)
                self.assertEqual(statement.operating_income, new_statement.operating_income)
                self.assertEqual(statement.operating_income_ratio, new_statement.operating_income_ratio)
                self.assertEqual(statement.other_expenses, new_statement.other_expenses)
                self.assertEqual(statement.research_and_development_expenses, new_statement.research_and_development_expenses)
                self.assertEqual(statement.revenue, new_statement.revenue)
                self.assertEqual(statement.selling_and_marketing_expenses, new_statement.selling_and_marketing_expenses)
                self.assertEqual(statement.selling_general_and_administrative_expenses, new_statement.selling_general_and_administrative_expenses)
                self.assertEqual(statement.total_other_income_expenses_net, new_statement.total_other_income_expenses_net)
                self.assertEqual(statement.weighted_average_shs_out, new_statement.weighted_average_shs_out)
                self.assertEqual(statement.weighted_average_shs_out_dil, new_statement.weighted_average_shs_out_dil)

    @parse_vcr.use_cassette("test_request_balance_sheets_finprep", filter_query_parameters=['apikey'])
    def test_create_balance_sheets_finprep(self):
        self.assertEqual(0, BalanceSheetFinprep.objects.all().count())
        self.parser.create_balance_sheets_finprep()
        self.assertEqual(5, BalanceSheetFinprep.objects.all().count())
        old_number_statements_created = BalanceSheetFinprep.objects.all().count()
        previous_list_data = [statement for statement in BalanceSheetFinprep.objects.all()]
        BalanceSheetFinprep.objects.all().delete()
        self.assertEqual(0, BalanceSheetFinprep.objects.all().count())
        for statement in finprep_data.BALANCE_SHEET:
            BalanceSheetFinprep.objects.create(
                **self.normalizer.normalize_balance_sheets_finprep(statement)
            )
        self.assertEqual(5, BalanceSheetFinprep.objects.all().count())
        self.assertEqual(old_number_statements_created, BalanceSheetFinprep.objects.all().count())
        for statement in previous_list_data:
            new_statement = BalanceSheetFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                self.assertEqual(statement.accepted_date, new_statement.accepted_date)
                self.assertEqual(statement.filling_date, new_statement.filling_date)
                self.assertEqual(statement.final_link, new_statement.final_link)
                self.assertEqual(statement.link, new_statement.link)
                self.assertEqual(statement.reported_currency, new_statement.reported_currency)
                self.assertEqual(statement.calendar_year, new_statement.calendar_year)
                self.assertEqual(statement.cik, new_statement.cik)
                self.assertEqual(statement.symbol, new_statement.symbol)
                self.assertEqual(statement.account_payables, new_statement.account_payables)
                self.assertEqual(statement.accumulated_other_comprehensive_income_loss, new_statement.accumulated_other_comprehensive_income_loss)
                self.assertEqual(statement.capital_lease_obligations, new_statement.capital_lease_obligations)
                self.assertEqual(statement.cash_and_cash_equivalents, new_statement.cash_and_cash_equivalents)
                self.assertEqual(statement.cash_and_short_term_investments, new_statement.cash_and_short_term_investments)
                self.assertEqual(statement.common_stock, new_statement.common_stock)
                self.assertEqual(statement.deferred_revenue, new_statement.deferred_revenue)
                self.assertEqual(statement.deferred_revenue_non_current, new_statement.deferred_revenue_non_current)
                self.assertEqual(statement.deferred_tax_liabilities_non_current, new_statement.deferred_tax_liabilities_non_current)
                self.assertEqual(statement.goodwill, new_statement.goodwill)
                self.assertEqual(statement.goodwill_and_intangible_assets, new_statement.goodwill_and_intangible_assets)
                self.assertEqual(statement.intangible_assets, new_statement.intangible_assets)
                self.assertEqual(statement.inventory, new_statement.inventory)
                self.assertEqual(statement.long_term_debt, new_statement.long_term_debt)
                self.assertEqual(statement.long_term_investments, new_statement.long_term_investments)
                self.assertEqual(statement.minority_interest, new_statement.minority_interest)
                self.assertEqual(statement.net_debt, new_statement.net_debt)
                self.assertEqual(statement.net_receivables, new_statement.net_receivables)
                self.assertEqual(statement.other_assets, new_statement.other_assets)
                self.assertEqual(statement.other_current_assets, new_statement.other_current_assets)
                self.assertEqual(statement.other_current_liabilities, new_statement.other_current_liabilities)
                self.assertEqual(statement.other_liabilities, new_statement.other_liabilities)
                self.assertEqual(statement.other_non_current_assets, new_statement.other_non_current_assets)
                self.assertEqual(statement.other_non_current_liabilities, new_statement.other_non_current_liabilities)
                self.assertEqual(statement.othertotal_stockholders_equity, new_statement.othertotal_stockholders_equity)
                self.assertEqual(statement.preferred_stock, new_statement.preferred_stock)
                self.assertEqual(statement.property_plant_equipment_net, new_statement.property_plant_equipment_net)
                self.assertEqual(statement.retained_earnings, new_statement.retained_earnings)
                self.assertEqual(statement.short_term_debt, new_statement.short_term_debt)
                self.assertEqual(statement.short_term_investments, new_statement.short_term_investments)
                self.assertEqual(statement.tax_assets, new_statement.tax_assets)
                self.assertEqual(statement.tax_payables, new_statement.tax_payables)
                self.assertEqual(statement.total_assets, new_statement.total_assets)
                self.assertEqual(statement.total_current_assets, new_statement.total_current_assets)
                self.assertEqual(statement.total_current_liabilities, new_statement.total_current_liabilities)
                self.assertEqual(statement.total_debt, new_statement.total_debt)
                self.assertEqual(statement.total_equity, new_statement.total_equity)
                self.assertEqual(statement.total_investments, new_statement.total_investments)
                self.assertEqual(statement.total_liabilities, new_statement.total_liabilities)
                self.assertEqual(statement.total_liabilities_and_stockholders_equity, new_statement.total_liabilities_and_stockholders_equity)
                self.assertEqual(statement.total_liabilities_and_total_equity, new_statement.total_liabilities_and_total_equity)
                self.assertEqual(statement.total_non_current_assets, new_statement.total_non_current_assets)
                self.assertEqual(statement.total_non_current_liabilities, new_statement.total_non_current_liabilities)
                self.assertEqual(statement.total_stockholders_equity, new_statement.total_stockholders_equity)

    @parse_vcr.use_cassette("test_request_cashflow_statements_finprep", filter_query_parameters=['apikey'])
    def test_create_cashflow_statements_finprep(self):
        self.assertEqual(0, CashflowStatementFinprep.objects.all().count())
        self.parser.create_cashflow_statements_finprep()
        self.assertEqual(5, CashflowStatementFinprep.objects.all().count())
        old_number_statements_created = CashflowStatementFinprep.objects.all().count()
        previous_list_data = [statement for statement in CashflowStatementFinprep.objects.all()]
        CashflowStatementFinprep.objects.all().delete()
        self.assertEqual(0, CashflowStatementFinprep.objects.all().count())
        for statement in finprep_data.CASHFLOW_STATEMENT:
            CashflowStatementFinprep.objects.create(
                **self.normalizer.normalize_cashflow_statements_finprep(statement)
            )
        self.assertEqual(5, CashflowStatementFinprep.objects.all().count())
        self.assertEqual(old_number_statements_created, CashflowStatementFinprep.objects.all().count())
        for statement in previous_list_data:
            new_statement = CashflowStatementFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                self.assertEqual(statement.accepted_date, new_statement.accepted_date)
                self.assertEqual(statement.filling_date, new_statement.filling_date)
                self.assertEqual(statement.final_link, new_statement.final_link)
                self.assertEqual(statement.link, new_statement.link)
                self.assertEqual(statement.reported_currency, new_statement.reported_currency)
                self.assertEqual(statement.calendar_year, new_statement.calendar_year)
                self.assertEqual(statement.cik, new_statement.cik)
                self.assertEqual(statement.symbol, new_statement.symbol)
                self.assertEqual(statement.accounts_payables, new_statement.accounts_payables)
                self.assertEqual(statement.accounts_receivables, new_statement.accounts_receivables)
                self.assertEqual(statement.acquisitions_net, new_statement.acquisitions_net)
                self.assertEqual(statement.capital_expenditure, new_statement.capital_expenditure)
                self.assertEqual(statement.cash_at_beginning_of_period, new_statement.cash_at_beginning_of_period)
                self.assertEqual(statement.cash_at_end_of_period, new_statement.cash_at_end_of_period)
                self.assertEqual(statement.change_in_working_capital, new_statement.change_in_working_capital)
                self.assertEqual(statement.common_stock_issued, new_statement.common_stock_issued)
                self.assertEqual(statement.common_stock_repurchased, new_statement.common_stock_repurchased)
                self.assertEqual(statement.debt_repayment, new_statement.debt_repayment)
                self.assertEqual(statement.deferred_income_tax, new_statement.deferred_income_tax)
                self.assertEqual(statement.depreciation_and_amortization, new_statement.depreciation_and_amortization)
                self.assertEqual(statement.dividends_paid, new_statement.dividends_paid)
                self.assertEqual(statement.effect_of_forex_changes_on_cash, new_statement.effect_of_forex_changes_on_cash)
                self.assertEqual(statement.free_cash_flow, new_statement.free_cash_flow)
                self.assertEqual(statement.inventory, new_statement.inventory)
                self.assertEqual(statement.investments_in_property_plant_and_equipment, new_statement.investments_in_property_plant_and_equipment)
                self.assertEqual(statement.net_cash_provided_by_operating_activities, new_statement.net_cash_provided_by_operating_activities)
                self.assertEqual(statement.net_cash_used_for_investing_activites, new_statement.net_cash_used_for_investing_activites)
                self.assertEqual(statement.net_cash_used_provided_by_financing_activities, new_statement.net_cash_used_provided_by_financing_activities)
                self.assertEqual(statement.net_change_in_cash, new_statement.net_change_in_cash)
                self.assertEqual(statement.net_income, new_statement.net_income)
                self.assertEqual(statement.operating_cash_flow, new_statement.operating_cash_flow)
                self.assertEqual(statement.other_financing_activites, new_statement.other_financing_activites)
                self.assertEqual(statement.other_investing_activites, new_statement.other_investing_activites)
                self.assertEqual(statement.other_non_cash_items, new_statement.other_non_cash_items)
                self.assertEqual(statement.other_working_capital, new_statement.other_working_capital)
                self.assertEqual(statement.purchases_of_investments, new_statement.purchases_of_investments)
                self.assertEqual(statement.sales_maturities_of_investments, new_statement.sales_maturities_of_investments)
                self.assertEqual(statement.stock_based_compensation, new_statement.stock_based_compensation)

    @parse_vcr.use_cassette("test_request_financials_finprep", filter_query_parameters=['apikey'])
    def test_create_financials_finprep(self):
        self.assertEqual(0, IncomeStatementFinprep.objects.all().count())
        self.assertEqual(0, BalanceSheetFinprep.objects.all().count())
        self.assertEqual(0, CashflowStatementFinprep.objects.all().count())
        self.parser.create_financials_finprep()
        self.assertEqual(5, IncomeStatementFinprep.objects.all().count())
        self.assertEqual(5, BalanceSheetFinprep.objects.all().count())
        self.assertEqual(5, CashflowStatementFinprep.objects.all().count())
        old_num_data_inc = IncomeStatementFinprep.objects.all().count()
        old_num_data_bs = BalanceSheetFinprep.objects.all().count()
        old_num_data_cf = CashflowStatementFinprep.objects.all().count()
        IncomeStatementFinprep.objects.all().delete()
        BalanceSheetFinprep.objects.all().delete()
        CashflowStatementFinprep.objects.all().delete()
        for statement in finprep_data.CASHFLOW_STATEMENT:
            CashflowStatementFinprep.objects.create(
                **self.normalizer.normalize_cashflow_statements_finprep(statement)
            )
        for statement in finprep_data.BALANCE_SHEET:
            BalanceSheetFinprep.objects.create(
                **self.normalizer.normalize_balance_sheets_finprep(statement)
            )
        for statement in finprep_data.INCOME_STATEMENT:
            IncomeStatementFinprep.objects.create(
                **self.normalizer.normalize_income_statements_finprep(statement)
            )
        self.assertEqual(old_num_data_inc, IncomeStatementFinprep.objects.all().count())
        self.assertEqual(old_num_data_bs, BalanceSheetFinprep.objects.all().count())
        self.assertEqual(old_num_data_cf, CashflowStatementFinprep.objects.all().count())
