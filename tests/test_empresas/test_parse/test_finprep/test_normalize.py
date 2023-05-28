from django.test import TestCase

from src.empresas.parse.finprep.normalize_data import NormalizeFinprep
from tests.data.empresas.finprep import finprep_data


class TestNormalizeFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = NormalizeFinprep()

    def test_normalize_income_statements_finprep(self):
        comp_data = self.parser.normalize_income_statements_finprep(
            finprep_data.INCOME_STATEMENT[0],
        )
        for field in [
            "accepted_date",
            "filling_date",
            "final_link",
            "link",
            "reported_currency",
            "calendar_year",
            "cik",
            "symbol",
            "cost_and_expenses",
            "cost_of_revenue",
            "depreciation_and_amortization",
            "ebitda",
            "ebitdaratio",
            "eps",
            "epsdiluted",
            "general_and_administrative_expenses",
            "gross_profit",
            "gross_profit_ratio",
            "income_before_tax",
            "income_before_tax_ratio",
            "income_tax_expense",
            "interest_expense",
            "interest_income",
            "net_income",
            "net_income_ratio",
            "operating_expenses",
            "operating_income",
            "operating_income_ratio",
            "other_expenses",
            "research_and_development_expenses",
            "revenue",
            "selling_and_marketing_expenses",
            "selling_general_and_administrative_expenses",
            "total_other_income_expenses_net",
            "weighted_average_shs_out",
            "weighted_average_shs_out_dil",
        ]:
            with self.subTest(field):
                self.assertTrue(field in comp_data)

    def test_normalize_balance_sheets_finprep(self):
        comp_data = self.parser.normalize_balance_sheets_finprep(
            finprep_data.BALANCE_SHEET[0],
        )
        for field in [
            "accepted_date",
            "filling_date",
            "final_link",
            "link",
            "reported_currency",
            "calendar_year",
            "cik",
            "symbol",
            "account_payables",
            "accumulated_other_comprehensive_income_loss",
            "capital_lease_obligations",
            "cash_and_cash_equivalents",
            "cash_and_short_term_investments",
            "common_stock",
            "deferred_revenue",
            "deferred_revenue_non_current",
            "deferred_tax_liabilities_non_current",
            "goodwill",
            "goodwill_and_intangible_assets",
            "intangible_assets",
            "inventory",
            "long_term_debt",
            "long_term_investments",
            "minority_interest",
            "net_debt",
            "net_receivables",
            "other_assets",
            "other_current_assets",
            "other_current_liabilities",
            "other_liabilities",
            "other_non_current_assets",
            "other_non_current_liabilities",
            "othertotal_stockholders_equity",
            "preferred_stock",
            "property_plant_equipment_net",
            "retained_earnings",
            "short_term_debt",
            "short_term_investments",
            "tax_assets",
            "tax_payables",
            "total_assets",
            "total_current_assets",
            "total_current_liabilities",
            "total_debt",
            "total_equity",
            "total_investments",
            "total_liabilities",
            "total_liabilities_and_stockholders_equity",
            "total_liabilities_and_total_equity",
            "total_non_current_assets",
            "total_non_current_liabilities",
            "total_stockholders_equity",
        ]:
            with self.subTest(field):
                self.assertTrue(field in comp_data)

    def test_normalize_cashflow_statements_finprep(self):
        comp_data = self.parser.normalize_cashflow_statements_finprep(
            finprep_data.CASHFLOW_STATEMENT[0],
        )
        for field in [
            "accepted_date",
            "filling_date",
            "final_link",
            "link",
            "reported_currency",
            "calendar_year",
            "cik",
            "symbol",
            "accounts_payables",
            "accounts_receivables",
            "acquisitions_net",
            "capital_expenditure",
            "cash_at_beginning_of_period",
            "cash_at_end_of_period",
            "change_in_working_capital",
            "common_stock_issued",
            "common_stock_repurchased",
            "debt_repayment",
            "deferred_income_tax",
            "depreciation_and_amortization",
            "dividends_paid",
            "effect_of_forex_changes_on_cash",
            "free_cash_flow",
            "inventory",
            "investments_in_property_plant_and_equipment",
            "net_cash_provided_by_operating_activities",
            "net_cash_used_for_investing_activites",
            "net_cash_used_provided_by_financing_activities",
            "net_change_in_cash",
            "net_income",
            "operating_cash_flow",
            "other_financing_activites",
            "other_investing_activites",
            "other_non_cash_items",
            "other_working_capital",
            "purchases_of_investments",
            "sales_maturities_of_investments",
            "stock_based_compensation",
        ]:
            with self.subTest(field):
                self.assertTrue(field in comp_data)
