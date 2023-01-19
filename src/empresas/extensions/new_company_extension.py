from typing import Dict, Union

from django.db.models import QuerySet

from src.empresas.models import Company
from src.general.utils import ChartSerializer


class CompanyData(ChartSerializer):
    company: Company

    def __init__(self, company: Company):
        self.company = company

    def get_complete_information(self) -> Dict[str, Dict[str, Union[int, float]]]:
        initial_statements = self.get_statements()
        statements_with_averages = self.get_averages(initial_statements)
        return statements_with_averages

    def get_statements(self) -> Dict[str, QuerySet]:
        # TODO add a prefetch to get all at once
        return {
            "inc_statements": self.company.inc_statements.yearly_exclude_ttm(),
            "balance_sheets": self.company.balance_sheets.yearly_exclude_ttm(),
            "cf_statements": self.company.cf_statements.yearly_exclude_ttm(),
            "rentability_ratios": self.company.rentability_ratios.yearly_exclude_ttm(),
            "liquidity_ratios": self.company.liquidity_ratios.yearly_exclude_ttm(),
            "margins": self.company.margins.yearly_exclude_ttm(),
            "fcf_ratios": self.company.fcf_ratios.yearly_exclude_ttm(),
            "per_share_values": self.company.per_share_values.yearly_exclude_ttm(),
            "non_gaap_figures": self.company.non_gaap_figures.yearly_exclude_ttm(),
            "operation_risks_ratios": self.company.operation_risks_ratios.yearly_exclude_ttm(),
            "ev_ratios": self.company.ev_ratios.yearly_exclude_ttm(),
            "growth_rates": self.company.growth_rates.yearly_exclude_ttm(),
            "efficiency_ratios": self.company.efficiency_ratios.yearly_exclude_ttm(),
            "price_to_ratios": self.company.price_to_ratios.yearly_exclude_ttm(),
        }

    @staticmethod
    def get_averages(statements: Dict[str, QuerySet]) -> Dict[str, Dict[str, Union[int, float]]]:
        # statements["inc_statements_averages"] = statements["inc_statements"].average_inc_statements()
        # statements["balance_sheets_averages"] = statements["balance_sheets"].average_balance_sheets()
        # statements["cf_statements_averages"] = statements["cf_statements"].average_cf_statements()
        statements["rentability_ratios_averages"] = statements["rentability_ratios"].average_rentability_ratios()
        statements["liquidity_ratios_averages"] = statements["liquidity_ratios"].average_liquidity_ratios()
        statements["margins_averages"] = statements["margins"].average_margins()
        # statements["fcf_ratios_averages"] = statements["fcf_ratios"].average_fcf_ratios()
        statements["per_share_values_averages"] = statements["per_share_values"].average_per_share_values()
        # statements["non_gaap_figures_averages"] = statements["non_gaap_figures"].average_non_gaap_figures()
        statements["operation_risks_ratios_averages"] = statements["operation_risks_ratios"].average_operation_risks_ratios()
        statements["ev_ratios_averages"] = statements["ev_ratios"].average_ev_ratios()
        statements["growth_rates_averages"] = statements["growth_rates"].average_growth_rates()
        statements["efficiency_ratios_averages"] = statements["efficiency_ratios"].average_efficiency_ratios()
        statements["price_to_ratios_averages"] = statements["price_to_ratios"].average_price_to_ratios()
        return statements

    @staticmethod
    def generate_limit(statement: QuerySet, limit: int) -> list:
        return statement[:limit] if limit != 0 else statement

    @staticmethod
    def build_table_and_chart(self, limit):
        comparing_json, rr = self.rentability_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, rr
