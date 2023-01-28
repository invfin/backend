import operator
from typing import Any, Callable, Dict, List, Optional, Union

from django.db.models import QuerySet

import yahooquery as yq
import yfinance as yf

from src.empresas.models import Company
from src.empresas.outils.company_to_json import CompanyValueToJsonConverter
from src.empresas.outils.financial_ratios.utils import calculate_compound_growth, divide_or_zero
from src.empresas.outils.valuations import discounted_cashflow, graham_value, margin_of_safety
from src.general.utils import ChartSerializer


class CompanyData(CompanyValueToJsonConverter):
    company: Company

    def __init__(self, company: Company, limit: int = 0):
        self.company = company
        self.limit = limit

    def get_complete_information(self) -> Dict[str, Union[Dict[str, Union[int, float]], List]]:
        initial_statements = self.get_statements()
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

    def get_ratios_information(self):
        initial_statements = self.get_statements()
        self.get_averages(initial_statements)
        return self.get_current_ratios(initial_statements)

    def get_statements(self) -> Dict[str, QuerySet]:
        # TODO add a prefetch to get all at once
        return {
            "inc_statements": self.company.inc_statements.yearly_exclude_ttm(),  # type: ignore
            "balance_sheets": self.company.balance_sheets.yearly_exclude_ttm(),  # type: ignore
            "cf_statements": self.company.cf_statements.yearly_exclude_ttm(),  # type: ignore
            "rentability_ratios": self.company.rentability_ratios.yearly_exclude_ttm(),  # type: ignore
            "liquidity_ratios": self.company.liquidity_ratios.yearly_exclude_ttm(),  # type: ignore
            "margins": self.company.margins.yearly_exclude_ttm(),  # type: ignore
            "fcf_ratios": self.company.fcf_ratios.yearly_exclude_ttm(),  # type: ignore
            "per_share_values": self.company.per_share_values.yearly_exclude_ttm(),  # type: ignore
            "non_gaap_figures": self.company.non_gaap_figures.yearly_exclude_ttm(),  # type: ignore
            "operation_risks_ratios": self.company.operation_risks_ratios.yearly_exclude_ttm(),  # type: ignore
            "ev_ratios": self.company.ev_ratios.yearly_exclude_ttm(),  # type: ignore
            "growth_rates": self.company.growth_rates.yearly_exclude_ttm(),  # type: ignore
            "efficiency_ratios": self.company.efficiency_ratios.yearly_exclude_ttm(),  # type: ignore
            "price_to_ratios": self.company.price_to_ratios.yearly_exclude_ttm(),  # type: ignore
        }

    @staticmethod
    def get_averages(
        statements: Dict[str, QuerySet],
    ) -> Dict[str, Union[QuerySet, Dict[str, Union[int, float]]]]:
        # statements["inc_statements_averages"] = statements[
        # "inc_statements"].average_inc_statements()
        # statements["balance_sheets_averages"] = statements[
        # "balance_sheets"].average_balance_sheets()
        # statements["cf_statements_averages"] = statements[
        # "cf_statements"].average_cf_statements()
        statements["averages"] = {
            **statements["rentability_ratios"].average_rentability_ratios(),  # type: ignore
            **statements["liquidity_ratios"].average_liquidity_ratios(),  # type: ignore
            **statements["margins"].average_margins(),  # type: ignore
            **statements["per_share_values"].average_per_share_values(),  # type: ignore
            **statements["operation_risks_ratios"].average_operation_risks_ratios(),  # type: ignore
            **statements["ev_ratios"].average_ev_ratios(),  # type: ignore
            **statements["growth_rates"].average_growth_rates(),  # type: ignore
            **statements["price_to_ratios"].average_price_to_ratios(),  # type: ignore
            **statements["efficiency_ratios"].average_efficiency_ratios(),  # type: ignore
        }  # type: ignore
        # statements["fcf_ratios_averages"] = statements["fcf_ratios"].average_fcf_ratios()
        # statements["non_gaap_figures_averages"] = statements[
        # "non_gaap_figures"].average_non_gaap_figures()
        return statements  # type: ignore

    def get_current_ratios(
        self,
        statements: Dict[str, QuerySet],
    ) -> dict:
        # TODO test
        averages = statements.pop("averages")
        current_price = self.get_most_recent_price(self.company.ticker)["current_price"]
        last_balance_sheet = statements["balance_sheets"].first()
        last_per_share = statements["per_share_values"].first()
        last_margins = statements["margins"].first()
        all_inc_statements = statements["inc_statements"]
        last_income_statement = all_inc_statements.first()
        last_revenue = last_income_statement.revenue or 0
        average_shares_out = last_income_statement.weighted_average_shares_outstanding or 0
        num_ics = min(all_inc_statements.count(), 10)
        number = num_ics - 1
        sharesbuyback = abs(
            calculate_compound_growth(
                average_shares_out,
                all_inc_statements[number].weighted_average_shares_outstanding,
                num_ics,
            )
        )
        cagr = calculate_compound_growth(last_revenue, all_inc_statements[number].revenue, num_ics)
        current_eps = last_per_share.eps or 0
        marketcap = average_shares_out * current_price
        pfcf = divide_or_zero(current_price, last_per_share.fcf_ps or 0)
        pb = divide_or_zero(current_price, last_per_share.book_ps or 0)
        pta = divide_or_zero(current_price, last_per_share.tangible_ps or 0)
        pcps = divide_or_zero(current_price, last_per_share.cash_ps or 0)
        pocf = divide_or_zero(current_price, last_per_share.operating_cf_ps or 0)
        per = divide_or_zero(current_price, current_eps)
        pas = divide_or_zero(current_price, last_per_share.total_assets_ps or 0)
        peg = divide_or_zero(per, cagr).real
        ps = divide_or_zero(current_price, last_per_share.sales_ps or 0)
        ev = marketcap + last_balance_sheet.total_debt or 0 - last_balance_sheet.cash_and_short_term_investments or 0
        evebitda = divide_or_zero(ev, last_income_statement.ebitda or 0)
        evsales = divide_or_zero(ev, last_revenue)
        gramvalu = graham_value(current_eps, last_per_share.book_ps or 0)
        safety_margin_pes = margin_of_safety(gramvalu, current_price)
        fair_value = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=cagr,
            net_income_margin=last_margins.net_income_margin or 0,
            fcf_margin=last_margins.fcf_margin or 0,
            buyback=sharesbuyback,
            average_shares_out=average_shares_out,
        )
        safety_margin_opt = margin_of_safety(fair_value, current_price)

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
        averages.update(
            {
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
            }
        )
        return averages

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

    def to_size_ratios(
        self,
        name: str,
        current: float,
        average: float,
        min_low: int,
        max_low: int,
        max_high: int,
        min_high_operator: Callable = operator.le,
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

    @classmethod
    def get_most_recent_price(cls, ticker):
        price, currency = cls.get_yfinance_price(ticker)
        if not price:
            price, currency = cls.get_yahooquery_price(ticker)
        if not price:
            price = 0
            currency = ""
        return {"current_price": price, "current_currency": currency}

    @staticmethod
    def get_yfinance_price(ticker):
        yfinance_info = yf.Ticker(ticker).info
        current_price = yfinance_info.get("currentPrice")
        current_currency = yfinance_info.get("currency")
        return current_price, current_currency

    @staticmethod
    def get_yahooquery_price(ticker):
        yahooquery_info = yq.Ticker(ticker).price.get(ticker, {})
        if yahooquery_info == f"Quote not found for ticker symbol: {ticker}":
            yahooquery_info = {}
        current_price = yahooquery_info.get("regularMarketPrice")
        current_currency = yahooquery_info.get("currency")
        return current_price, current_currency
