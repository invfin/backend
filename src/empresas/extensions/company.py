


import yahooquery as yq
import yfinance as yf

from src.empresas.outils.valuations import discounted_cashflow
from src.general.utils import ChartSerializer


class CompanyExtended(ChartSerializer):
    currency_to_use = None

    def find_currency(self, statement):
        if not self.currency:
            try:
                currency = statement[0].reported_currency
            except Exception:
                currency = None
            else:
                self.currency = currency
                self.save(update_fields=["currency"])
        else:
            currency = self.currency
        if currency:
            self.currency_to_use = currency.currency
            return currency.currency
        return "$"

    def all_income_statements(self, limit) -> list:
        inc = self.inc_statements.yearly_exclude_ttm()
        if limit != 0:
            inc = inc[:limit]
        return inc

    def income_json(self, limit):
        inc = self.all_income_statements(limit)
        if not self.currency_to_use:
            currency = self.find_currency(inc)
        else:
            currency = self.currency_to_use
        inc_json = {
            "currency": currency,
            "labels": [data.date_year for data in inc],
            "fields": [
                {
                    "title": "Ingresos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.revenue for data in inc],
                },
                {
                    "title": "Costos de venta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cost_of_revenue for data in inc],
                },
                {
                    "title": "Utilidad bruta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.gross_profit for data in inc],
                },
                {
                    "title": "I&D",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.rd_expenses for data in inc],
                },
                {
                    "title": "Gastos administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.general_administrative_expenses for data in inc],
                },
                {
                    "title": "Gastos marketing",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.selling_marketing_expenses for data in inc],
                },
                {
                    "title": "Gastos marketing, generales y administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.sga_expenses for data in inc],
                },
                {
                    "title": "Gastos otros",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_expenses for data in inc],
                },
                {
                    "title": "Gastos operativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_expenses for data in inc],
                },
                {
                    "title": "Gastos y costos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cost_and_expenses for data in inc],
                },
                {
                    "title": "Intereses",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.interest_expense for data in inc],
                },
                {
                    "title": "Depreciación & Amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.depreciation_amortization for data in inc],
                },
                {
                    "title": "EBITDA",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.ebitda for data in inc],
                },
                {
                    "title": "Ingresos de explotación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_income for data in inc],
                },
                {
                    "title": "Otros Gastos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_total_other_income_expenses for data in inc],
                },
                {
                    "title": "EBT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.income_before_tax for data in inc],
                },
                {
                    "title": "Impuestos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.income_tax_expenses for data in inc],
                },
                {
                    "title": "Ingresos netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_income for data in inc],
                },
                {
                    "title": "Acciones en circulación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.weighted_average_shares_outstanding for data in inc],
                },
                {
                    "title": "Acciones diluidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.weighted_average_diluated_shares_outstanding for data in inc],
                },
            ],
        }
        return inc_json, inc

    def comparing_income_json(self, limit):
        comparing_json, inc = self.income_json(limit)
        chartData = self.generate_json(comparing_json)
        self.generate_json(comparing_json, [0, 18], "bar")
        data = {"table": comparing_json, "chart": chartData}
        return data, inc

    def all_balance_sheets(self, limit) -> list:
        bls = self.balance_sheets.yearly_exclude_ttm()
        if limit != 0:
            bls = bls[:limit]
        return bls

    def comparing_balance_json(self, limit):
        comparing_json, bls = self.balance_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, bls

    def all_cashflow_statements(self, limit) -> list:
        cf = self.cf_statements.yearly_exclude_ttm()
        if limit != 0:
            cf = cf[:limit]
        return cf

    def comparing_cashflows(self, limit):
        comparing_json, cf = self.cashflow_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_rentablity_ratios(self, limit) -> list:
        rr = self.rentability_ratios.yearly_exclude_ttm()
        if limit != 0:
            rr = rr[:limit]
        return rr

    def comparing_rentability_ratios_json(self, limit):
        comparing_json, rr = self.rentability_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, rr

    def all_liquidity_ratios(self, limit) -> list:
        lr = self.liquidity_ratios.yearly_exclude_ttm()
        if limit != 0:
            lr = lr[:limit]
        return lr

    def comparing_liquidity_ratios_json(self, limit):
        comparing_json, lr = self.liquidity_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, lr

    def all_margins(self, limit) -> list:
        margins = self.margins.yearly_exclude_ttm()
        if limit != 0:
            margins = margins[:limit]
        return margins

    def comparing_margins_json(self, limit):
        comparing_json, cf = self.margins_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_fcf_ratios(self, limit) -> list:
        fcf_ratios = self.fcf_ratios.yearly_exclude_ttm()
        if limit != 0:
            fcf_ratios = fcf_ratios[:limit]
        return fcf_ratios

    def comparing_fcf_ratios_json(self, limit):
        comparing_json, cf = self.fcf_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_per_share_values(self, limit) -> list:
        per_share_values = self.per_share_values.yearly_exclude_ttm()
        if limit != 0:
            per_share_values = per_share_values[:limit]
        return per_share_values

    def comparing_per_share_values_json(self, limit):
        comparing_json, cf = self.per_share_values_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_non_gaap(self, limit) -> list:
        nongaap = self.non_gaap_figures.yearly_exclude_ttm()
        if limit != 0:
            nongaap = nongaap[:limit]
        return nongaap

    def comparing_non_gaap_json(self, limit):
        comparing_json, nongaap = self.non_gaap_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, nongaap

    def all_operation_risks_ratios(self, limit) -> list:
        operation_risks_ratios = self.operation_risks_ratios.yearly_exclude_ttm()
        if limit != 0:
            operation_risks_ratios = operation_risks_ratios[:limit]
        return operation_risks_ratios

    def comparing_operation_risks_ratios_json(self, limit):
        comparing_json, cf = self.operation_risks_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_ev_ratios(self, limit) -> list:
        ev_ratios = self.ev_ratios.yearly_exclude_ttm()
        if limit != 0:
            ev_ratios = ev_ratios[:limit]
        return ev_ratios

    def comparing_ev_ratios_json(self, limit):
        comparing_json, ev_ratios = self.ev_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, ev_ratios

    def all_growth_rates(self, limit) -> list:
        growth_rates = self.growth_rates.yearly_exclude_ttm()
        if limit != 0:
            growth_rates = growth_rates[:limit]
        return growth_rates

    def comparing_growth_rates_json(self, limit):
        comparing_json, cf = self.growth_rates_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_efficiency_ratios(self, limit) -> list:
        efficiency_ratios = self.efficiency_ratios.yearly_exclude_ttm()
        if limit != 0:
            efficiency_ratios = efficiency_ratios[:limit]
        return efficiency_ratios

    def efficiency_ratios_json(self, limit):
        cf = self.all_efficiency_ratios(limit)
        er_json = {
            "labels": [data.date_year for data in cf],
            "fields": [
                {
                    "title": "Rotación de activos",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.asset_turnover for data in cf],
                },
                {
                    "title": "Rotación del inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.inventory_turnover for data in cf],
                },
                {
                    "title": "Rotación de activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.fixed_asset_turnover for data in cf],
                },
                {
                    "title": "Rotación de cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.accounts_payable_turnover for data in cf],
                },
                {
                    "title": "Ciclo conversión de efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_conversion_cycle for data in cf],
                },
                {
                    "title": "Inventario disponible (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_inventory_outstanding for data in cf],
                },
                {
                    "title": "Cuentas por pagar en circulación (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_payables_outstanding for data in cf],
                },
                {
                    "title": "Ventas activas (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_sales_outstanding for data in cf],
                },
                {
                    "title": "Ratio FCF a flujo de efectivo operativo",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.free_cashflow_to_operating_cashflow for data in cf],
                },
                {
                    "title": "Ciclo operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.operating_cycle for data in cf],
                },
            ],
        }
        return er_json, cf

    def comparing_efficiency_ratios_json(self, limit):
        comparing_json, cf = self.efficiency_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def all_price_to_ratios(self, limit) -> list:
        price_to_ratios = self.price_to_ratios.yearly_exclude_ttm()
        if limit != 0:
            price_to_ratios = price_to_ratios[:limit]
        return price_to_ratios

    def price_to_ratios_json(self, limit):
        cf = self.all_price_to_ratios(limit)
        cf_json = {
            "labels": [data.date_year for data in cf],
            "fields": [
                {
                    "title": "Precio valor en libros",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_book for data in cf],
                },
                {
                    "title": "Precio cashflow",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_cf for data in cf],
                },
                {
                    "title": "Precio beneficio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_earnings for data in cf],
                },
                {
                    "title": "PEG",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_earnings_growth for data in cf],
                },
                {
                    "title": "Precio por ventas",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_sales for data in cf],
                },
                {
                    "title": "Precio activos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_total_assets for data in cf],
                },
                {
                    "title": "Precio FCF",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_fcf for data in cf],
                },
                {
                    "title": "Precio cashflow operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_operating_cf for data in cf],
                },
                {
                    "title": "Precio activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_tangible_assets for data in cf],
                },
            ],
        }
        return cf_json, cf

    def comparing_price_to_ratios_json(self, limit):
        comparing_json, cf = self.price_to_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {"table": comparing_json, "chart": chartData}
        return data, cf

    def important_ratios(self, limit):
        comparing_rentability_ratios_json, rentability_ratios = self.comparing_rentability_ratios_json(limit)
        comparing_liquidity_ratios_json, liquidity_ratios = self.comparing_liquidity_ratios_json(limit)
        comparing_margins_json, margins = self.comparing_margins_json(limit)

        ratios = [
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
        query_ratios = {
            "rentability_ratios": rentability_ratios,
            "liquidity_ratios": liquidity_ratios,
            "margins": margins,
        }
        return ratios, query_ratios

    def secondary_ratios(self, limit):
        comparing_efficiency_ratios_json, efficiency_ratios = self.comparing_efficiency_ratios_json(limit)
        comparing_operation_risks_ratios_json, op_risk_ratios = self.comparing_operation_risks_ratios_json(limit)
        comparing_non_gaap_json, non_gaap = self.comparing_non_gaap_json(limit)
        comparing_per_share_values_json, per_share = self.comparing_per_share_values_json(limit)
        comparing_fcf_ratios_json, fcf_ratios = self.comparing_fcf_ratios_json(limit)

        ratios = [
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
        query_ratios = {
            "efficiency_ratios": efficiency_ratios,
            "op_risk_ratios": op_risk_ratios,
            "non_gaap": non_gaap,
            "per_share": per_share,
            "fcf_ratios": fcf_ratios,
        }
        return ratios, query_ratios



    def get_most_recent_price(self):
        yfinance_info = yf.Ticker(self.ticker).info
        if "currentPrice" in yfinance_info:
            current_price = yfinance_info["currentPrice"]
            current_currency = yfinance_info["currency"]
        else:
            yahooquery_info = yq.Ticker(self.ticker).price
            key = list(yahooquery_info.keys())[0]
            if yahooquery_info[key] != "Quote not found for ticker symbol: LB":
                current_price = yahooquery_info[key]["regularMarketPrice"]
                current_currency = yahooquery_info[key]["currency"]
            else:
                current_price = 0
                current_currency = ""
        return {"current_price": current_price, "current_currency": current_currency}



    def complete_info(self, limit=10):
        comparing_income_json, all_inc_statements = self.comparing_income_json(limit)
        comparing_balance_json, all_balance_sheets = self.comparing_balance_json(limit)
        comparing_cashflows, all_cashflow_statements = self.comparing_cashflows(limit)
        important_ratios, all_important_ratios = self.important_ratios(limit)
        secondary_ratios, all_secondary_ratios = self.secondary_ratios(limit)

        all_important_ratios["rentability_ratios"]
        all_important_ratios["liquidity_ratios"]
        all_important_ratios["margins"]

        all_secondary_ratios["efficiency_ratios"]
        all_secondary_ratios["op_risk_ratios"]
        all_secondary_ratios["non_gaap"]
        all_secondary_ratios["per_share"]
        all_secondary_ratios["fcf_ratios"]

        comparing_ev_ratios_json, all_ev_ratios = self.comparing_ev_ratios_json(limit)
        comparing_growth_rates_json, all_growth_rates = self.comparing_growth_rates_json(limit)

        try:
            marketcap = all_ev_ratios[0].market_cap
        except IndexError:
            marketcap = 0
        return {
            "comparing_income_json": comparing_income_json,
            "comparing_balance_json": comparing_balance_json,
            "comparing_cashflows": comparing_cashflows,
            "important_ratios": important_ratios,
            "secondary_ratios": secondary_ratios,
            "marketcap": marketcap,
        }
