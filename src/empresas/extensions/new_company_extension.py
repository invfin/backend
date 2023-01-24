import math
import operator

from typing import Any, Callable, Dict, Union, List, Type

from django.db.models import QuerySet

from src.empresas.models import Company
from src.empresas.outils.company_to_json import CompanyValueToJsonConverter
from src.general.utils import ChartSerializer


class CompanyData(CompanyValueToJsonConverter):
    company: Company

    def __init__(self, company: Company):
        self.company = company

    def get_complete_information(self) -> Dict[str, Union[Dict[str, Union[int, float]], List]]:
        initial_statements = self.get_statements()
        self.get_averages(initial_statements)
        comparing_income_json = self.build_table_and_chart(initial_statements["inc_statements"], self.income_json,)
        comparing_balance_json = self.build_table_and_chart(initial_statements["balance_sheets"], self.balance_json,)
        comparing_cashflows = self.build_table_and_chart(initial_statements["cf_statements"], self.cashflow_json,)
        return {
            "comparing_income_json": comparing_income_json,
            "comparing_balance_json": comparing_balance_json,
            "comparing_cashflows": comparing_cashflows,
            "important_ratios": self.get_important_ratios(initial_statements),
            "secondary_ratios": self.get_secondary_ratios(initial_statements),
        }

    def get_important_ratios(self, statements: Dict) -> List:
        comparing_rentability_ratios_json = self.build_table_and_chart(statements["rentability_ratios"], self.rentability_ratios_json,)
        comparing_liquidity_ratios_json = self.build_table_and_chart(statements["liquidity_ratios"], self.liquidity_ratios_json,)
        comparing_margins_json = self.build_table_and_chart(statements["margins"], self.margins_json,)

        return [
            {
                "kind": "rentability",
                "title": "Ratios de rentabilidad",
                "table": comparing_rentability_ratios_json["table"],
                "chart": comparing_rentability_ratios_json["chart"],
            },
            {
                "kind": "liquidity",
                "title": "Ratios de liquidez",
                "table": comparing_liquidity_ratios_json["table"],
                "chart": comparing_liquidity_ratios_json["chart"],
            },
            {
                "kind": "margins",
                "title": "Márgenes",
                "table": comparing_margins_json["table"],
                "chart": comparing_margins_json["chart"],
            },
        ]

    def get_secondary_ratios(self, statements: Dict) -> List:
        comparing_efficiency_ratios_json = self.build_table_and_chart(statements["efficiency_ratios"], self.efficiency_ratios_json,)
        comparing_operation_risks_ratios_json = self.build_table_and_chart(statements["operation_risks_ratios"], self.operation_risks_ratios_json,)
        comparing_non_gaap_json = self.build_table_and_chart(statements["non_gaap_figures"], self.non_gaap_json,)
        comparing_per_share_values_json = self.build_table_and_chart(statements["per_share_values"], self.per_share_values_json,)
        comparing_fcf_ratios_json = self.build_table_and_chart(statements["fcf_ratios"], self.fcf_ratios_json,)

        return [
            {
                "kind": "efficiency",
                "title": "Ratios de eficiencia",
                "table": comparing_efficiency_ratios_json["table"],
                "chart": comparing_efficiency_ratios_json["chart"],
            },
            {
                "kind": "operations",
                "title": "Ratios de riesgo de operaciones",
                "table": comparing_operation_risks_ratios_json["table"],
                "chart": comparing_operation_risks_ratios_json["chart"],
            },
            {
                "kind": "nongaap",
                "title": "Non GAAP",
                "table": comparing_non_gaap_json["table"],
                "chart": comparing_non_gaap_json["chart"],
            },
            {
                "kind": "pershare",
                "title": "Valor por acción",
                "table": comparing_per_share_values_json["table"],
                "chart": comparing_per_share_values_json["chart"],
            },
            {
                "kind": "fcfratios",
                "title": "FCF ratios",
                "table": comparing_fcf_ratios_json["table"],
                "chart": comparing_fcf_ratios_json["chart"],
            },
        ]

    def get_statements(self) -> Dict[str, QuerySet]:
        # TODO add a prefetch to get all at once
        return {
            "inc_statements": self.company.inc_statements.yearly_exclude_ttm(), #type: ignore
            "balance_sheets": self.company.balance_sheets.yearly_exclude_ttm(), #type: ignore
            "cf_statements": self.company.cf_statements.yearly_exclude_ttm(), #type: ignore
            "rentability_ratios": self.company.rentability_ratios.yearly_exclude_ttm(), #type: ignore
            "liquidity_ratios": self.company.liquidity_ratios.yearly_exclude_ttm(), #type: ignore
            "margins": self.company.margins.yearly_exclude_ttm(), #type: ignore
            "fcf_ratios": self.company.fcf_ratios.yearly_exclude_ttm(), #type: ignore
            "per_share_values": self.company.per_share_values.yearly_exclude_ttm(), #type: ignore
            "non_gaap_figures": self.company.non_gaap_figures.yearly_exclude_ttm(), #type: ignore
            "operation_risks_ratios": self.company.operation_risks_ratios.yearly_exclude_ttm(), #type: ignore
            "ev_ratios": self.company.ev_ratios.yearly_exclude_ttm(), #type: ignore
            "growth_rates": self.company.growth_rates.yearly_exclude_ttm(), #type: ignore
            "efficiency_ratios": self.company.efficiency_ratios.yearly_exclude_ttm(), #type: ignore
            "price_to_ratios": self.company.price_to_ratios.yearly_exclude_ttm(), #type: ignore
        }

    @staticmethod
    def get_averages(statements: Dict[str, QuerySet]) -> Dict[str, Union[QuerySet,Dict[str, Union[int, float]]]]:
        # statements["inc_statements_averages"] = statements[
        # "inc_statements"].average_inc_statements()
        # statements["balance_sheets_averages"] = statements[
        # "balance_sheets"].average_balance_sheets()
        # statements["cf_statements_averages"] = statements[
        # "cf_statements"].average_cf_statements()
        statements["rentability_ratios_averages"] = statements["rentability_ratios"].average_rentability_ratios() #type: ignore
        statements["liquidity_ratios_averages"] = statements["liquidity_ratios"].average_liquidity_ratios() #type: ignore
        statements["margins_averages"] = statements["margins"].average_margins() #type: ignore
        # statements["fcf_ratios_averages"] = statements["fcf_ratios"].average_fcf_ratios()
        statements["per_share_values_averages"] = statements["per_share_values"].average_per_share_values() #type: ignore
        # statements["non_gaap_figures_averages"] = statements[
        # "non_gaap_figures"].average_non_gaap_figures()
        statements["operation_risks_ratios_averages"] = statements[
            "operation_risks_ratios"
        ].average_operation_risks_ratios() #type: ignore
        statements["ev_ratios_averages"] = statements["ev_ratios"].average_ev_ratios() #type: ignore
        statements["growth_rates_averages"] = statements["growth_rates"].average_growth_rates() #type: ignore
        statements["efficiency_ratios_averages"] = statements["efficiency_ratios"].average_efficiency_ratios() #type: ignore
        statements["price_to_ratios_averages"] = statements["price_to_ratios"].average_price_to_ratios() #type: ignore
        return statements #type: ignore

    @staticmethod
    def generate_limit(statement: QuerySet, limit: int) -> list:
        return statement[:limit] if limit != 0 else statement #type: ignore

    @staticmethod
    def build_table_and_chart(
        statement_data: QuerySet,
        statement_to_json: Callable,
        items: list = None,
        chart_type: str = "line",
    ) -> Dict[str, Any]:
        comparing_json = statement_to_json(statement_data)
        return {
            "table": comparing_json,
            "chart": ChartSerializer.generate_json(comparing_json, items, chart_type),
        }

    def calculate_current_ratios(
        self,
        all_balance_sheets: list = None,
        all_per_share: list = None,
        all_margins: list = None,
        all_inc_statements: list = None,
        all_efficiency_ratios: list = None,
        all_growth_rates: list = None,
        all_per_share_values: list = None,
        all_price_to_ratios: list = None,
        all_liquidity_ratios: list = None,
        all_rentablity_ratios: list = None,
        all_operation_risks_ratios: list = None,
        all_ev_ratios: list = None,
    ) -> dict:
        current_price = self.get_most_recent_price()["current_price"]

        all_balance_sheets = all_balance_sheets if all_balance_sheets else self.all_balance_sheets(
            10)
        all_per_share = all_per_share if all_per_share else self.all_per_share_values(10)
        all_margins = all_margins if all_margins else self.all_margins(10)
        all_inc_statements = all_inc_statements if all_inc_statements else self.all_income_statements(
            10)
        all_efficiency_ratios = all_efficiency_ratios if all_efficiency_ratios else self.all_efficiency_ratios(
            10)
        all_growth_rates = all_growth_rates if all_growth_rates else self.all_growth_rates(10)
        all_per_share_values = all_per_share_values if all_per_share_values else self.all_per_share_values(
            10)
        all_price_to_ratios = all_price_to_ratios if all_price_to_ratios else self.all_price_to_ratios(
            10)
        all_liquidity_ratios = all_liquidity_ratios if all_liquidity_ratios else self.all_liquidity_ratios(
            10)
        all_rentablity_ratios = all_rentablity_ratios if all_rentablity_ratios else self.all_rentablity_ratios(
            10)
        all_operation_risks_ratios = (
            all_operation_risks_ratios if all_operation_risks_ratios else self.all_operation_risks_ratios(
                10)
        )
        all_ev_ratios = all_ev_ratios if all_ev_ratios else self.all_ev_ratios(10)
        averages = self.calculate_averages(
            all_margins,
            all_efficiency_ratios,
            all_growth_rates,
            all_per_share_values,
            all_price_to_ratios,
            all_liquidity_ratios,
            all_rentablity_ratios,
            all_operation_risks_ratios,
            all_ev_ratios,
        )
        last_balance_sheet = all_balance_sheets[0]
        last_per_share = all_per_share[0]
        last_margins = all_margins[0]
        last_income_statement = all_inc_statements[0]
        last_revenue = last_income_statement.revenue
        average_shares_out = last_income_statement.weighted_average_shares_outstanding

        num_ics = 10 if len(all_inc_statements) >= 10 else len(all_inc_statements)
        number = num_ics - 1

        try:
            sharesbuyback = abs(
                (
                    (
                        (average_shares_out / all_inc_statements[
                            number].weighted_average_shares_outstanding)
                        ** ((1 / num_ics))
                    )
                    - 1
                )
                * 100
            )
        except ZeroDivisionError:
            sharesbuyback = 0

        try:
            cagr = (((last_revenue / all_inc_statements[number].revenue) ** (
            (1 / num_ics))) - 1) * 100
        except ZeroDivisionError:
            cagr = 0
        current_eps = last_per_share.eps
        marketcap = average_shares_out * current_price

        try:
            pfcf = current_price / last_per_share.fcf_ps
        except ZeroDivisionError:
            pfcf = 0

        try:
            pb = current_price / last_per_share.book_ps
        except ZeroDivisionError:
            pb = 0

        try:
            pta = current_price / last_per_share.tangible_ps
        except ZeroDivisionError:
            pta = 0

        try:
            pcps = current_price / last_per_share.cash_ps
        except ZeroDivisionError:
            pcps = 0

        try:
            pocf = current_price / last_per_share.operating_cf_ps
        except ZeroDivisionError:
            pocf = 0

        try:
            per = current_price / current_eps
        except ZeroDivisionError:
            per = 0

        try:
            pas = current_price / last_per_share.total_assets_ps
        except ZeroDivisionError:
            pas = 0

        try:
            peg = (per / cagr).real
        except ZeroDivisionError:
            peg = 0

        try:
            ps = current_price / last_per_share.sales_ps
        except ZeroDivisionError:
            ps = 0

        ev = marketcap + last_balance_sheet.total_debt - last_balance_sheet.cash_and_short_term_investments

        try:
            evebitda = ev / last_income_statement.ebitda
        except ZeroDivisionError:
            evebitda = 0

        try:
            evsales = ev / last_revenue
        except ZeroDivisionError:
            evsales = 0

        try:
            gramvalu = (
                math.sqrt(22.5 * current_eps * last_per_share.book_ps)) if current_eps > 0 else 0
        except ValueError:
            gramvalu = 0
        safety_margin_pes = ((gramvalu / current_price) - 1) * 100 if current_price != 0 else 0

        fair_value = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=cagr,
            net_income_margin=last_margins.net_income_margin,
            fcf_margin=last_margins.fcf_margin,
            buyback=sharesbuyback,
            average_shares_out=average_shares_out,
        )
        safety_margin_opt = ((fair_value / current_price) - 1) * 100 if current_price != 0 else 0

        most_used_ratios = [
            {
                "name": "PER",
                "current": per,
                "average": averages.get("average_price_earnings"),
                "min_low": 15,
                "max_low": 30,
                "max_high": 30,
                "min_high_operator": operator.le,
            },
            {
                "name": "PB",
                "current": pb,
                "average": averages.get("average_price_book"),
                "min_low": 2,
                "max_low": 3,
                "max_high": 3,
                "min_high_operator": operator.le,
            },
            {
                "name": "PS",
                "current": ps,
                "average": averages.get("average_price_sales"),
                "min_low": 2,
                "max_low": 4,
                "max_high": 4,
                "min_high_operator": operator.le,
            },
            {
                "name": "PFCF",
                "current": pfcf,
                "average": averages.get("average_price_fcf"),
                "min_low": 15,
                "max_low": 30,
                "max_high": 30,
                "min_high_operator": operator.eq,
            },
            {
                "name": "PEG",
                "current": peg,
                "average": averages.get("average_price_earnings_growth"),
                "min_low": 1,
                "max_low": 2,
                "max_high": 2,
                "min_high_operator": operator.le,
            },
            {
                "name": "Precio Activos Totales",
                "current": pas,
                "average": averages.get("average_price_total_assets"),
                "min_low": 2,
                "max_low": 3,
                "max_high": 6,
                "min_high_operator": operator.le,
            },
            {
                "name": "Precio Activos Tangibles",
                "current": pta,
                "average": averages.get("average_price_tangible_assets"),
                "min_low": 2,
                "max_low": 3,
                "max_high": 3,
                "min_high_operator": operator.le,
            },
            {
                "name": "Precio Efectivo",
                "current": pcps,
                "average": averages.get("average_price_cf"),
                "min_low": 2,
                "max_low": 5,
                "max_high": 10,
                "min_high_operator": operator.le,
            },
            {
                "name": "Precio Flujo efectivo operativo",
                "current": pocf,
                "average": averages.get("average_price_operating_cf"),
                "min_low": 10,
                "max_low": 18,
                "max_high": 25,
                "min_high_operator": operator.le,
            },
            {
                "name": "EV/EBITDA",
                "current": evebitda,
                "average": averages.get("average_ev_multiple"),
                "min_low": 15,
                "max_low": 30,
                "max_high": 30,
                "min_high_operator": operator.le,
            },
            {
                "name": "EV/SALES",
                "current": evsales,
                "average": averages.get("average_ev_sales"),
                "min_low": 1,
                "max_low": 4,
                "max_high": 4,
                "min_high_operator": operator.le,
            },
        ]

        most_used_ratios = [self.to_size_ratios(**valuation) for valuation in most_used_ratios]

        return {
            "most_used_ratios": most_used_ratios,
            "pfcf": pfcf,
            "pas": pas,
            "pta": pta,
            "pcps": pcps,
            "pocf": pocf,
            "per": per,
            "pb": pb,
            "peg": peg,
            "ps": ps,
            "fair_value": fair_value,
            "ev": ev,
            "marketcap": marketcap,
            "cagr": cagr,
            "evebitda": evebitda,
            "evsales": evsales,
            "gramvalu": gramvalu,
            "sharesbuyback": sharesbuyback,
            "safety_margin_pes": safety_margin_pes,
            "safety_margin_opt": safety_margin_opt,
            "current_price": current_price,
            "last_revenue": last_revenue,
            "average_shares_out": average_shares_out,
            "last_balance_sheet": last_balance_sheet,
            "last_per_share": last_per_share,
            "last_margins": last_margins,
            "last_income_statement": last_income_statement,
            **averages,
        }

    def to_size_ratios(
        self,
        name: str,
        current: float,
        average: float,
        min_low: int,
        max_low: int,
        max_high: int,
        min_high_operator: Type[operator] = operator.le,
    ) -> dict:
        valuation_result = {
            "name": name,
            "current_value": current,
            "average_value": average,
        }

        if current > max_high or min_high_operator(current, 0):
            valuation_result["current_veredict"] = "Sobrevalorado"
            valuation_result["current_color"] = "danger"
        elif current < max_low and current > min_low:
            valuation_result["current_veredict"] = "Neutral"
            valuation_result["current_color"] = "warning"
        else:
            valuation_result["current_veredict"] = "Infravalorado"
            valuation_result["current_color"] = "success"

        if current > average + 3:
            valuation_result["average_veredict"] = "Sobrevalorado"
            valuation_result["average_color"] = "danger"
        elif current < average + 3:
            valuation_result["average_veredict"] = "Infravalorado"
            valuation_result["average_color"] = "success"
        else:
            valuation_result["average_veredict"] = "Neutral"
            valuation_result["average_color"] = "warning"
        return valuation_result

    def get_currency(self, statement: QuerySet) -> str:
        if not self.company.currency:
            try:
                currency = statement[0].reported_currency
            except Exception:
                currency = None
            else:
                self.company.currency = currency
                self.company.save(update_fields=["currency"])
        else:
            currency = self.company.currency
        return currency.currency if currency else "$"
