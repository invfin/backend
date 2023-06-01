import operator
from typing import Any, Callable, Dict, List, Optional, Union

from django.db.models import QuerySet

from src.general.utils import ChartSerializer


from .company_to_json import CompanyValueToJsonConverter


class CompanyChartPresentation(CompanyValueToJsonConverter):
    def get_complete_information(
        self, initial_statements
    ) -> Dict[str, Union[Dict[str, Union[int, float]], List]]:
        comparing_income_json = self.build_table_and_chart(
            initial_statements["inc_statements"],
            self.income_json,
        )
        comparing_balance_json = self.build_table_and_chart(
            initial_statements["balance_sheets"],
            self.balance_json,
        )
        comparing_cashflows = self.build_table_and_chart(
            initial_statements["cf_statements"],
            self.cashflow_json,
        )
        return {
            "comparing_income_json": comparing_income_json,
            "comparing_balance_json": comparing_balance_json,
            "comparing_cashflows": comparing_cashflows,
            "important_ratios": self.get_important_ratios(initial_statements),
            "secondary_ratios": self.get_secondary_ratios(initial_statements),
        }

    def compare_most_used_ratios(
        self,
        per: Union[int, float],
        pb: Union[int, float],
        ps: Union[int, float],
        pfcf: Union[int, float],
        peg: Union[int, float],
        pas: Union[int, float],
        pcps: Union[int, float],
        pta: Union[int, float],
        pocf: Union[int, float],
        evebitda: Union[int, float],
        evsales: Union[int, float],
        averages: Dict[str, Union[int, float]],
    ) -> List[Dict[str, Any]]:
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
        return [self.to_size_ratios(**valuation) for valuation in most_used_ratios]

    def to_size_ratios(
        self,
        name: str,
        current: float,
        average: float,
        min_low: int,
        max_low: int,
        max_high: int,
        min_high_operator: Callable = operator.le,
    ) -> Dict[str, Union[str, int, float]]:
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

    def get_important_ratios(self, statements: Dict) -> List:
        comparing_rentability_ratios_json = self.build_table_and_chart(
            statements["rentability_ratios"],
            self.rentability_ratios_json,
        )
        comparing_liquidity_ratios_json = self.build_table_and_chart(
            statements["liquidity_ratios"],
            self.liquidity_ratios_json,
        )
        comparing_margins_json = self.build_table_and_chart(
            statements["margins"],
            self.margins_json,
        )

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
        comparing_efficiency_ratios_json = self.build_table_and_chart(
            statements["efficiency_ratios"],
            self.efficiency_ratios_json,
        )
        comparing_operation_risks_ratios_json = self.build_table_and_chart(
            statements["operation_risks_ratios"],
            self.operation_risks_ratios_json,
        )
        comparing_non_gaap_json = self.build_table_and_chart(
            statements["non_gaap_figures"],
            self.non_gaap_json,
        )
        comparing_per_share_values_json = self.build_table_and_chart(
            statements["per_share_values"],
            self.per_share_values_json,
        )
        comparing_fcf_ratios_json = self.build_table_and_chart(
            statements["fcf_ratios"],
            self.fcf_ratios_json,
        )

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

    def generate_limit(self, statement: QuerySet) -> list:
        return statement[: self.limit] if self.limit != 0 else statement  # type: ignore

    def build_table_and_chart(
        self,
        statement: QuerySet,
        statement_to_json: Callable,
        items: Optional[list] = None,
        chart_type: str = "line",
    ) -> Dict[str, Any]:
        statement_data = self.generate_limit(statement)
        comparing_json = statement_to_json(statement_data)
        return {
            "table": comparing_json,
            "chart": ChartSerializer.generate_json(comparing_json, items, chart_type),
        }
