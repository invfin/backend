import vcr

from django.test import TestCase

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import BalanceSheetFinprep, IncomeStatementFinprep, CashflowStatementFinprep, Company
from apps.empresas.parse.finprep import FinprepInfo
from apps.empresas.parse.finprep.normalize_data import NormalizeFinprep
from apps.empresas.parse.finprep.parse_data import ParseFinprep
from tests.data import finprep_data


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/finprep/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()

    @parse_vcr.use_cassette(filter_query_parameters=["apikey"])
    def test_request_income_statements_finprep(self):
        comp_data = self.parser.request_income_statements_finprep("AAPL")
        assert finprep_data.INCOME_STATEMENT == comp_data

    @parse_vcr.use_cassette(filter_query_parameters=["apikey"])
    def test_request_balance_sheets_finprep(self):
        comp_data = self.parser.request_balance_sheets_finprep("AAPL")
        assert finprep_data.BALANCE_SHEET == comp_data

    @parse_vcr.use_cassette(filter_query_parameters=["apikey"])
    def test_request_cashflow_statements_finprep(self):
        comp_data = self.parser.request_cashflow_statements_finprep("AAPL")
        assert finprep_data.CASHFLOW_STATEMENT == comp_data

    @parse_vcr.use_cassette(filter_query_parameters=["apikey"])
    def test_request_financials_finprep(self):
        comp_data = self.parser.request_financials_finprep("AAPL")
        assert finprep_data.DICT_STATEMENTS == comp_data


class TestNormalizeFinprep(TestCase):
    def setUpTestData(cls) -> None:
        cls.parser = NormalizeFinprep()
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser.company = cls.company
        cls.income_statement = finprep_data.INCOME_STATEMENT[0]
        cls.balance_sheet = finprep_data.BALANCE_SHEET[0]
        cls.cashflow_statement = finprep_data.CASHFLOW_STATEMENT[0]

    def test_normalize_income_statements_finprep(self):
        comp_data = self.parser.normalize_income_statements_finprep(self.income_statement)
        assert ("accepted_date" in comp_data) is True
        assert ("filling_date" in comp_data) is True
        assert ("final_link" in comp_data) is True
        assert ("link" in comp_data) is True
        assert ("reported_currency" in comp_data) is True
        assert ("calendar_year" in comp_data) is True
        assert ("cik" in comp_data) is True
        assert ("symbol" in comp_data) is True
        assert ("cost_and_expenses" in comp_data) is True
        assert ("cost_of_revenue" in comp_data) is True
        assert ("depreciation_and_amortization" in comp_data) is True
        assert ("ebitda" in comp_data) is True
        assert ("ebitdaratio" in comp_data) is True
        assert ("eps" in comp_data) is True
        assert ("epsdiluted" in comp_data) is True
        assert ("general_and_administrative_expenses" in comp_data) is True
        assert ("gross_profit" in comp_data) is True
        assert ("gross_profit_ratio" in comp_data) is True
        assert ("income_before_tax" in comp_data) is True
        assert ("income_before_tax_ratio" in comp_data) is True
        assert ("income_tax_expense" in comp_data) is True
        assert ("interest_expense" in comp_data) is True
        assert ("interest_income" in comp_data) is True
        assert ("net_income" in comp_data) is True
        assert ("net_income_ratio" in comp_data) is True
        assert ("operating_expenses" in comp_data) is True
        assert ("operating_income" in comp_data) is True
        assert ("operating_income_ratio" in comp_data) is True
        assert ("other_expenses" in comp_data) is True
        assert ("research_and_development_expenses" in comp_data) is True
        assert ("revenue" in comp_data) is True
        assert ("selling_and_marketing_expenses" in comp_data) is True
        assert ("selling_general_and_administrative_expenses" in comp_data) is True
        assert ("total_other_income_expenses_net" in comp_data) is True
        assert ("weighted_average_shs_out" in comp_data) is True
        assert ("weighted_average_shs_out_dil" in comp_data) is True

    def test_normalize_balance_sheets_finprep(self):
        comp_data = self.parser.normalize_balance_sheets_finprep(self.balance_sheet)
        assert ("accepted_date" in comp_data) is True
        assert ("filling_date" in comp_data) is True
        assert ("final_link" in comp_data) is True
        assert ("link" in comp_data) is True
        assert ("reported_currency" in comp_data) is True
        assert ("calendar_year" in comp_data) is True
        assert ("cik" in comp_data) is True
        assert ("symbol" in comp_data) is True
        assert ("account_payables" in comp_data) is True
        assert ("accumulated_other_comprehensive_income_loss" in comp_data) is True
        assert ("capital_lease_obligations" in comp_data) is True
        assert ("cash_and_cash_equivalents" in comp_data) is True
        assert ("cash_and_short_term_investments" in comp_data) is True
        assert ("common_stock" in comp_data) is True
        assert ("deferred_revenue" in comp_data) is True
        assert ("deferred_revenue_non_current" in comp_data) is True
        assert ("deferred_tax_liabilities_non_current" in comp_data) is True
        assert ("goodwill" in comp_data) is True
        assert ("goodwill_and_intangible_assets" in comp_data) is True
        assert ("intangible_assets" in comp_data) is True
        assert ("inventory" in comp_data) is True
        assert ("long_term_debt" in comp_data) is True
        assert ("long_term_investments" in comp_data) is True
        assert ("minority_interest" in comp_data) is True
        assert ("net_debt" in comp_data) is True
        assert ("net_receivables" in comp_data) is True
        assert ("other_assets" in comp_data) is True
        assert ("other_current_assets" in comp_data) is True
        assert ("other_current_liabilities" in comp_data) is True
        assert ("other_liabilities" in comp_data) is True
        assert ("other_non_current_assets" in comp_data) is True
        assert ("other_non_current_liabilities" in comp_data) is True
        assert ("othertotal_stockholders_equity" in comp_data) is True
        assert ("preferred_stock" in comp_data) is True
        assert ("property_plant_equipment_net" in comp_data) is True
        assert ("retained_earnings" in comp_data) is True
        assert ("short_term_debt" in comp_data) is True
        assert ("short_term_investments" in comp_data) is True
        assert ("tax_assets" in comp_data) is True
        assert ("tax_payables" in comp_data) is True
        assert ("total_assets" in comp_data) is True
        assert ("total_current_assets" in comp_data) is True
        assert ("total_current_liabilities" in comp_data) is True
        assert ("total_debt" in comp_data) is True
        assert ("total_equity" in comp_data) is True
        assert ("total_investments" in comp_data) is True
        assert ("total_liabilities" in comp_data) is True
        assert ("total_liabilities_and_stockholders_equity" in comp_data) is True
        assert ("total_liabilities_and_total_equity" in comp_data) is True
        assert ("total_non_current_assets" in comp_data) is True
        assert ("total_non_current_liabilities" in comp_data) is True
        assert ("total_stockholders_equity" in comp_data) is True

    def test_normalize_cashflow_statements_finprep(self):
        comp_data = self.parser.normalize_cashflow_statements_finprep(self.cashflow_statement)
        assert ("accepted_date" in comp_data) is True
        assert ("filling_date" in comp_data) is True
        assert ("final_link" in comp_data) is True
        assert ("link" in comp_data) is True
        assert ("reported_currency" in comp_data) is True
        assert ("calendar_year" in comp_data) is True
        assert ("cik" in comp_data) is True
        assert ("symbol" in comp_data) is True
        assert ("accounts_payables" in comp_data) is True
        assert ("accounts_receivables" in comp_data) is True
        assert ("acquisitions_net" in comp_data) is True
        assert ("capital_expenditure" in comp_data) is True
        assert ("cash_at_beginning_of_period" in comp_data) is True
        assert ("cash_at_end_of_period" in comp_data) is True
        assert ("change_in_working_capital" in comp_data) is True
        assert ("common_stock_issued" in comp_data) is True
        assert ("common_stock_repurchased" in comp_data) is True
        assert ("debt_repayment" in comp_data) is True
        assert ("deferred_income_tax" in comp_data) is True
        assert ("depreciation_and_amortization" in comp_data) is True
        assert ("dividends_paid" in comp_data) is True
        assert ("effect_of_forex_changes_on_cash" in comp_data) is True
        assert ("free_cash_flow" in comp_data) is True
        assert ("inventory" in comp_data) is True
        assert ("investments_in_property_plant_and_equipment" in comp_data) is True
        assert ("net_cash_provided_by_operating_activities" in comp_data) is True
        assert ("net_cash_used_for_investing_activites" in comp_data) is True
        assert ("net_cash_used_provided_by_financing_activities" in comp_data) is True
        assert ("net_change_in_cash" in comp_data) is True
        assert ("net_income" in comp_data) is True
        assert ("operating_cash_flow" in comp_data) is True
        assert ("other_financing_activites" in comp_data) is True
        assert ("other_investing_activites" in comp_data) is True
        assert ("other_non_cash_items" in comp_data) is True
        assert ("other_working_capital" in comp_data) is True
        assert ("purchases_of_investments" in comp_data) is True
        assert ("sales_maturities_of_investments" in comp_data) is True
        assert ("stock_based_compensation" in comp_data) is True


class TestFinprepInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DTM.create(Company, ticker="AAPL")
        cls.parser = FinprepInfo(cls.company)
        cls.normalizer = NormalizeFinprep()

    @parse_vcr.use_cassette("test_request_income_statements_finprep", filter_query_parameters=["apikey"])
    def test_create_income_statements_finprep(self):
        assert 0 == IncomeStatementFinprep.objects.all().count()
        self.parser.create_income_statements_finprep()
        assert 5 == IncomeStatementFinprep.objects.all().count()
        old_number_statements_created = IncomeStatementFinprep.objects.all().count()
        previous_list_data = [statement for statement in IncomeStatementFinprep.objects.all()]
        IncomeStatementFinprep.objects.all().delete()
        assert 0 == IncomeStatementFinprep.objects.all().count()
        for statement in finprep_data.INCOME_STATEMENT:
            IncomeStatementFinprep.objects.create(**self.normalizer.normalize_income_statements_finprep(statement))
        assert 5 == IncomeStatementFinprep.objects.all().count()
        assert (old_number_statements_created== IncomeStatementFinprep.objects.all().count())
        for statement in previous_list_data:
            new_statement = IncomeStatementFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                assert statement.accepted_date == new_statement.accepted_date
                assert statement.filling_date == new_statement.filling_date
                assert statement.final_link == new_statement.final_link
                assert statement.link == new_statement.link
                assert statement.reported_currency == new_statement.reported_currency
                assert statement.calendar_year == new_statement.calendar_year
                assert statement.cik == new_statement.cik
                assert statement.symbol == new_statement.symbol
                assert statement.cost_and_expenses == new_statement.cost_and_expenses
                assert statement.cost_of_revenue == new_statement.cost_of_revenue
                assert statement.depreciation_and_amortization == new_statement.depreciation_and_amortization
                assert statement.ebitda == new_statement.ebitda
                assert statement.ebitdaratio == new_statement.ebitdaratio
                assert statement.eps == new_statement.eps
                assert statement.epsdiluted == new_statement.epsdiluted
                assert (
                    statement.general_and_administrative_expenses == new_statement.general_and_administrative_expenses
                )
                assert statement.gross_profit == new_statement.gross_profit
                assert statement.gross_profit_ratio == new_statement.gross_profit_ratio
                assert statement.income_before_tax == new_statement.income_before_tax
                assert statement.income_before_tax_ratio == new_statement.income_before_tax_ratio
                assert statement.income_tax_expense == new_statement.income_tax_expense
                assert statement.interest_expense == new_statement.interest_expense
                assert statement.interest_income == new_statement.interest_income
                assert statement.net_income == new_statement.net_income
                assert statement.net_income_ratio == new_statement.net_income_ratio
                assert statement.operating_expenses == new_statement.operating_expenses
                assert statement.operating_income == new_statement.operating_income
                assert statement.operating_income_ratio == new_statement.operating_income_ratio
                assert statement.other_expenses == new_statement.other_expenses
                assert statement.research_and_development_expenses == new_statement.research_and_development_expenses
                assert statement.revenue == new_statement.revenue
                assert statement.selling_and_marketing_expenses == new_statement.selling_and_marketing_expenses
                assert (
                    statement.selling_general_and_administrative_expenses
                    == new_statement.selling_general_and_administrative_expenses
                )
                assert statement.total_other_income_expenses_net == new_statement.total_other_income_expenses_net
                assert statement.weighted_average_shs_out == new_statement.weighted_average_shs_out
                assert statement.weighted_average_shs_out_dil == new_statement.weighted_average_shs_out_dil

    @parse_vcr.use_cassette("test_request_balance_sheets_finprep", filter_query_parameters=["apikey"])
    def test_create_balance_sheets_finprep(self):
        assert 0 == BalanceSheetFinprep.objects.all().count()
        self.parser.create_balance_sheets_finprep()
        assert 5 == BalanceSheetFinprep.objects.all().count()
        old_number_statements_created = BalanceSheetFinprep.objects.all().count()
        previous_list_data = [statement for statement in BalanceSheetFinprep.objects.all()]
        BalanceSheetFinprep.objects.all().delete()
        assert 0 == BalanceSheetFinprep.objects.all().count()
        for statement in finprep_data.BALANCE_SHEET:
            BalanceSheetFinprep.objects.create(**self.normalizer.normalize_balance_sheets_finprep(statement))
        assert 5 == BalanceSheetFinprep.objects.all().count()
        assert old_number_statements_created == BalanceSheetFinprep.objects.all().count()
        for statement in previous_list_data:
            new_statement = BalanceSheetFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                assert statement.accepted_date == new_statement.accepted_date
                assert statement.filling_date == new_statement.filling_date
                assert statement.final_link == new_statement.final_link
                assert statement.link == new_statement.link
                assert statement.reported_currency == new_statement.reported_currency
                assert statement.calendar_year == new_statement.calendar_year
                assert statement.cik == new_statement.cik
                assert statement.symbol == new_statement.symbol
                assert statement.account_payables == new_statement.account_payables
                assert (
                    statement.accumulated_other_comprehensive_income_loss
                    == new_statement.accumulated_other_comprehensive_income_loss
                )
                assert statement.capital_lease_obligations == new_statement.capital_lease_obligations
                assert statement.cash_and_cash_equivalents == new_statement.cash_and_cash_equivalents
                assert statement.cash_and_short_term_investments == new_statement.cash_and_short_term_investments
                assert statement.common_stock == new_statement.common_stock
                assert statement.deferred_revenue == new_statement.deferred_revenue
                assert statement.deferred_revenue_non_current == new_statement.deferred_revenue_non_current
                assert (
                    statement.deferred_tax_liabilities_non_current == new_statement.deferred_tax_liabilities_non_current
                )
                assert statement.goodwill == new_statement.goodwill
                assert statement.goodwill_and_intangible_assets == new_statement.goodwill_and_intangible_assets
                assert statement.intangible_assets == new_statement.intangible_assets
                assert statement.inventory == new_statement.inventory
                assert statement.long_term_debt == new_statement.long_term_debt
                assert statement.long_term_investments == new_statement.long_term_investments
                assert statement.minority_interest == new_statement.minority_interest
                assert statement.net_debt == new_statement.net_debt
                assert statement.net_receivables == new_statement.net_receivables
                assert statement.other_assets == new_statement.other_assets
                assert statement.other_current_assets == new_statement.other_current_assets
                assert statement.other_current_liabilities == new_statement.other_current_liabilities
                assert statement.other_liabilities == new_statement.other_liabilities
                assert statement.other_non_current_assets == new_statement.other_non_current_assets
                assert statement.other_non_current_liabilities == new_statement.other_non_current_liabilities
                assert statement.othertotal_stockholders_equity == new_statement.othertotal_stockholders_equity
                assert statement.preferred_stock == new_statement.preferred_stock
                assert statement.property_plant_equipment_net == new_statement.property_plant_equipment_net
                assert statement.retained_earnings == new_statement.retained_earnings
                assert statement.short_term_debt == new_statement.short_term_debt
                assert statement.short_term_investments == new_statement.short_term_investments
                assert statement.tax_assets == new_statement.tax_assets
                assert statement.tax_payables == new_statement.tax_payables
                assert statement.total_assets == new_statement.total_assets
                assert statement.total_current_assets == new_statement.total_current_assets
                assert statement.total_current_liabilities == new_statement.total_current_liabilities
                assert statement.total_debt == new_statement.total_debt
                assert statement.total_equity == new_statement.total_equity
                assert statement.total_investments == new_statement.total_investments
                assert statement.total_liabilities == new_statement.total_liabilities
                assert (
                    statement.total_liabilities_and_stockholders_equity
                    == new_statement.total_liabilities_and_stockholders_equity
                )
                assert statement.total_liabilities_and_total_equity == new_statement.total_liabilities_and_total_equity
                assert statement.total_non_current_assets == new_statement.total_non_current_assets
                assert statement.total_non_current_liabilities == new_statement.total_non_current_liabilities
                assert statement.total_stockholders_equity == new_statement.total_stockholders_equity

    @parse_vcr.use_cassette("test_request_cashflow_statements_finprep", filter_query_parameters=["apikey"])
    def test_create_cashflow_statements_finprep(self):
        assert 0 == CashflowStatementFinprep.objects.all().count()
        self.parser.create_cashflow_statements_finprep()
        assert 5 == CashflowStatementFinprep.objects.all().count()
        old_number_statements_created = CashflowStatementFinprep.objects.all().count()
        previous_list_data = [statement for statement in CashflowStatementFinprep.objects.all()]
        CashflowStatementFinprep.objects.all().delete()
        assert 0 == CashflowStatementFinprep.objects.all().count()
        for statement in finprep_data.CASHFLOW_STATEMENT:
            CashflowStatementFinprep.objects.create(**self.normalizer.normalize_cashflow_statements_finprep(statement))
        assert 5 == CashflowStatementFinprep.objects.all().count()
        assert old_number_statements_created == CashflowStatementFinprep.objects.all().count()
        for statement in previous_list_data:
            new_statement = CashflowStatementFinprep.objects.get(date=statement.date)
            with self.subTest(statement):
                assert statement.accepted_date == new_statement.accepted_date
                assert statement.filling_date == new_statement.filling_date
                assert statement.final_link == new_statement.final_link
                assert statement.link == new_statement.link
                assert statement.reported_currency == new_statement.reported_currency
                assert statement.calendar_year == new_statement.calendar_year
                assert statement.cik == new_statement.cik
                assert statement.symbol == new_statement.symbol
                assert statement.accounts_payables == new_statement.accounts_payables
                assert statement.accounts_receivables == new_statement.accounts_receivables
                assert statement.acquisitions_net == new_statement.acquisitions_net
                assert statement.capital_expenditure == new_statement.capital_expenditure
                assert statement.cash_at_beginning_of_period == new_statement.cash_at_beginning_of_period
                assert statement.cash_at_end_of_period == new_statement.cash_at_end_of_period
                assert statement.change_in_working_capital == new_statement.change_in_working_capital
                assert statement.common_stock_issued == new_statement.common_stock_issued
                assert statement.common_stock_repurchased == new_statement.common_stock_repurchased
                assert statement.debt_repayment == new_statement.debt_repayment
                assert statement.deferred_income_tax == new_statement.deferred_income_tax
                assert statement.depreciation_and_amortization == new_statement.depreciation_and_amortization
                assert statement.dividends_paid == new_statement.dividends_paid
                assert statement.effect_of_forex_changes_on_cash == new_statement.effect_of_forex_changes_on_cash
                assert statement.free_cash_flow == new_statement.free_cash_flow
                assert statement.inventory == new_statement.inventory
                assert (
                    statement.investments_in_property_plant_and_equipment
                    == new_statement.investments_in_property_plant_and_equipment
                )
                assert (
                    statement.net_cash_provided_by_operating_activities
                    == new_statement.net_cash_provided_by_operating_activities
                )
                assert (
                    statement.net_cash_used_for_investing_activites
                    == new_statement.net_cash_used_for_investing_activites
                )
                assert (
                    statement.net_cash_used_provided_by_financing_activities
                    == new_statement.net_cash_used_provided_by_financing_activities
                )
                assert statement.net_change_in_cash == new_statement.net_change_in_cash
                assert statement.net_income == new_statement.net_income
                assert statement.operating_cash_flow == new_statement.operating_cash_flow
                assert statement.other_financing_activites == new_statement.other_financing_activites
                assert statement.other_investing_activites == new_statement.other_investing_activites
                assert statement.other_non_cash_items == new_statement.other_non_cash_items
                assert statement.other_working_capital == new_statement.other_working_capital
                assert statement.purchases_of_investments == new_statement.purchases_of_investments
                assert statement.sales_maturities_of_investments == new_statement.sales_maturities_of_investments
                assert statement.stock_based_compensation == new_statement.stock_based_compensation

    @parse_vcr.use_cassette("test_request_financials_finprep", filter_query_parameters=["apikey"])
    def test_create_financials_finprep(self):
        assert 0 == IncomeStatementFinprep.objects.all().count()
        assert 0 == BalanceSheetFinprep.objects.all().count()
        assert 0 == CashflowStatementFinprep.objects.all().count()
        self.parser.create_financials_finprep()
        assert 5 == IncomeStatementFinprep.objects.all().count()
        assert 5 == BalanceSheetFinprep.objects.all().count()
        assert 5 == CashflowStatementFinprep.objects.all().count()
        old_num_data_inc = IncomeStatementFinprep.objects.all().count()
        old_num_data_bs = BalanceSheetFinprep.objects.all().count()
        old_num_data_cf = CashflowStatementFinprep.objects.all().count()
        IncomeStatementFinprep.objects.all().delete()
        BalanceSheetFinprep.objects.all().delete()
        CashflowStatementFinprep.objects.all().delete()
        for statement in finprep_data.CASHFLOW_STATEMENT:
            CashflowStatementFinprep.objects.create(**self.normalizer.normalize_cashflow_statements_finprep(statement))
        for statement in finprep_data.BALANCE_SHEET:
            BalanceSheetFinprep.objects.create(**self.normalizer.normalize_balance_sheets_finprep(statement))
        for statement in finprep_data.INCOME_STATEMENT:
            IncomeStatementFinprep.objects.create(**self.normalizer.normalize_income_statements_finprep(statement))
        assert old_num_data_inc == IncomeStatementFinprep.objects.all().count()
        assert old_num_data_bs == BalanceSheetFinprep.objects.all().count()
        assert old_num_data_cf == CashflowStatementFinprep.objects.all().count()
