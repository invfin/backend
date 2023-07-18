from django.db.models import QuerySet


class CompanyValueToJsonConverter:
    """
    Used to generate JSON formated data from the company to create charts
    """

    def get_currency(self, statement):
        # TODO: replace for a better one
        try:
            currency = statement[0].reported_currency.symbol
        except Exception:
            currency = None
        return currency or "$"

    def income_json(self, statement: QuerySet):
        return {
            "currency": self.get_currency(statement),
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Ingresos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.revenue for data in statement],
                },
                {
                    "title": "Costos de venta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cost_of_revenue for data in statement],
                },
                {
                    "title": "Utilidad bruta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.gross_profit for data in statement],
                },
                {
                    "title": "I&D",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.rd_expenses for data in statement],
                },
                {
                    "title": "Gastos administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.general_administrative_expenses for data in statement],
                },
                {
                    "title": "Gastos marketing",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.selling_marketing_expenses for data in statement],
                },
                {
                    "title": "Gastos marketing, generales y administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.sga_expenses for data in statement],
                },
                {
                    "title": "Gastos otros",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_expenses for data in statement],
                },
                {
                    "title": "Gastos operativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_expenses for data in statement],
                },
                {
                    "title": "Gastos y costos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cost_and_expenses for data in statement],
                },
                {
                    "title": "Intereses",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.interest_expense for data in statement],
                },
                {
                    "title": "Depreciación & Amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.depreciation_amortization for data in statement],
                },
                {
                    "title": "EBITDA",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.ebitda for data in statement],
                },
                {
                    "title": "Ingresos de explotación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_income for data in statement],
                },
                {
                    "title": "Otros Gastos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_total_other_income_expenses for data in statement],
                },
                {
                    "title": "EBT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.income_before_tax for data in statement],
                },
                {
                    "title": "Impuestos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.income_tax_expenses for data in statement],
                },
                {
                    "title": "Ingresos netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_income for data in statement],
                },
                {
                    "title": "Acciones en circulación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.weighted_average_shares_outstanding for data in statement],
                },
                {
                    "title": "Acciones diluidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [
                        data.weighted_average_diluated_shares_outstanding for data in statement
                    ],
                },
            ],
        }

    def balance_json(self, statement: QuerySet):
        return {
            "currency": self.get_currency(statement),
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Efectivo y equivalentes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cash_and_cash_equivalents for data in statement],
                },
                {
                    "title": "Inversiones corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.short_term_investments for data in statement],
                },
                {
                    "title": "Efectivo e inversiones corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cash_and_short_term_investments for data in statement],
                },
                {
                    "title": "Cuentas por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_receivables for data in statement],
                },
                {
                    "title": "Inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.inventory for data in statement],
                },
                {
                    "title": "Otro activos corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_current_assets for data in statement],
                },
                {
                    "title": "Activos corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_current_assets for data in statement],
                },
                {
                    "title": "Propiedades y equipamiento",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.property_plant_equipment for data in statement],
                },
                {
                    "title": "Goodwill",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.goodwill for data in statement],
                },
                {
                    "title": "Activos intangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.intangible_assets for data in statement],
                },
                {
                    "title": "Goodwill y activos intangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.goodwill_and_intangible_assets for data in statement],
                },
                {
                    "title": "Inversiones a largo plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.long_term_investments for data in statement],
                },
                {
                    "title": "Impuestos retenidos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.tax_assets for data in statement],
                },
                {
                    "title": "Otros activos no corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_non_current_assets for data in statement],
                },
                {
                    "title": "Activos no corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_non_current_assets for data in statement],
                },
                {
                    "title": "Otros activos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_assets for data in statement],
                },
                {
                    "title": "Activos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_assets for data in statement],
                },
                {
                    "title": "Cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.accounts_payable for data in statement],
                },
                {
                    "title": "Deuda a corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.short_term_debt for data in statement],
                },
                {
                    "title": "Impuestos por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.tax_payables for data in statement],
                },
                {
                    "title": "Ingreso diferido",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.deferred_revenue for data in statement],
                },
                {
                    "title": "Otros pasivos corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_current_liabilities for data in statement],
                },
                {
                    "title": "Pasivos corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_current_liabilities for data in statement],
                },
                {
                    "title": "Deuda a largo plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.long_term_debt for data in statement],
                },
                {
                    "title": "Otros ingresos por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.deferred_revenue_non_current for data in statement],
                },
                {
                    "title": "Otros impuestos por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [
                        data.deferred_tax_liabilities_non_current for data in statement
                    ],
                },
                {
                    "title": "Otros pasivos no corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_non_current_liabilities for data in statement],
                },
                {
                    "title": "Pasivos no corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_non_current_liabilities for data in statement],
                },
                {
                    "title": "Otros pasivos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_liabilities for data in statement],
                },
                {
                    "title": "Pasivos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_liabilities for data in statement],
                },
                {
                    "title": "Ingresos para accionistas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.common_stocks for data in statement],
                },
                {
                    "title": "Ganancias retenidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.retained_earnings for data in statement],
                },
                {
                    "title": "Otras pérdidas acumuladas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [
                        data.accumulated_other_comprehensive_income_loss for data in statement
                    ],
                },
                {
                    "title": "Otra equidad total",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.othertotal_stockholders_equity for data in statement],
                },
                {
                    "title": "Equidad de los accionistas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_stockholders_equity for data in statement],
                },
                {
                    "title": "Equidad y deuda totalas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_liabilities_and_total_equity for data in statement],
                },
                {
                    "title": "Inversiones totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_investments for data in statement],
                },
                {
                    "title": "Deuda total",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.total_debt for data in statement],
                },
                {
                    "title": "Deuda neta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_debt for data in statement],
                },
            ],
        }

    def cashflow_json(self, statement: QuerySet):
        return {
            "currency": self.get_currency(statement),
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Beneficio neto",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_income for data in statement],
                },
                {
                    "title": "Depreciación y amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.depreciation_amortization for data in statement],
                },
                {
                    "title": "Impuesto sobre beneficio diferido",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.deferred_income_tax for data in statement],
                },
                {
                    "title": "Compensación en acciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.stock_based_compensation for data in statement],
                },
                {
                    "title": "Cambios en working capital",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.change_in_working_capital for data in statement],
                },
                {
                    "title": "Cuentas por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.accounts_receivable for data in statement],
                },
                {
                    "title": "Inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.inventory for data in statement],
                },
                {
                    "title": "Cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.accounts_payable for data in statement],
                },
                {
                    "title": "Otro working capital",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_working_capital for data in statement],
                },
                {
                    "title": "Otras utilidades no en efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_non_cash_items for data in statement],
                },
                {
                    "title": "Flujo de caja de las operaciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_activities_cf for data in statement],
                },
                {
                    "title": "Inversiones en plantas y equipamiento",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [
                        data.investments_property_plant_equipment for data in statement
                    ],
                },
                {
                    "title": "Adquisiciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.acquisitions_net for data in statement],
                },
                {
                    "title": "Inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.purchases_investments for data in statement],
                },
                {
                    "title": "Ingresos por venta de inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.sales_maturities_investments for data in statement],
                },
                {
                    "title": "Otras inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_investing_activites for data in statement],
                },
                {
                    "title": "Flujo de caja dedicado a inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.investing_activities_cf for data in statement],
                },
                {
                    "title": "Pago de deudas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.debt_repayment for data in statement],
                },
                {
                    "title": "Acciones emitidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.common_stock_issued for data in statement],
                },
                {
                    "title": "Recompra de acciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.common_stock_repurchased for data in statement],
                },
                {
                    "title": "Dividendos pagados",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.dividends_paid for data in statement],
                },
                {
                    "title": "Otras actividades financieras",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.other_financing_activities for data in statement],
                },
                {
                    "title": "Flujo de caja usado (proporcionado) por actividades financieras",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.financing_activities_cf for data in statement],
                },
                {
                    "title": "Efecto del cambio de divisas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.effect_forex_exchange for data in statement],
                },
                {
                    "title": "Cambio en efectivo neto",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_change_cash for data in statement],
                },
                {
                    "title": "Efectivo al final del periodo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cash_end_period for data in statement],
                },
                {
                    "title": "Efectivo al principio del periodo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.cash_beginning_period for data in statement],
                },
                {
                    "title": "Flujo de caja operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.operating_cf for data in statement],
                },
                {
                    "title": "CAPEX",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.capex for data in statement],
                },
                {
                    "title": "Flujo de caja libre",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.fcf for data in statement],
                },
            ],
        }

    @staticmethod
    def efficiency_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Rotación de activos",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.asset_turnover for data in statement],
                },
                {
                    "title": "Rotación del inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.inventory_turnover for data in statement],
                },
                {
                    "title": "Rotación de activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.fixed_asset_turnover for data in statement],
                },
                {
                    "title": "Rotación de cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.accounts_payable_turnover for data in statement],
                },
                {
                    "title": "Ciclo conversión de efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_conversion_cycle for data in statement],
                },
                {
                    "title": "Inventario disponible (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_inventory_outstanding for data in statement],
                },
                {
                    "title": "Cuentas por pagar en circulación (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_payables_outstanding for data in statement],
                },
                {
                    "title": "Ventas activas (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.days_sales_outstanding for data in statement],
                },
                {
                    "title": "Ratio FCF a flujo de efectivo operativo",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.free_cashflow_to_operating_cashflow for data in statement],
                },
                {
                    "title": "Ciclo operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.operating_cycle for data in statement],
                },
            ],
        }

    @staticmethod
    def ev_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Capitalización bursátil",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.market_cap for data in statement],
                },
                {
                    "title": "Enterprise value",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.enterprise_value for data in statement],
                },
                {
                    "title": "EV to free cash flow",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.ev_fcf for data in statement],
                },
                {
                    "title": "EV to operating cashflow",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.ev_operating_cf for data in statement],
                },
                {
                    "title": "EV to sales",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.ev_sales for data in statement],
                },
                {
                    "title": "Equity multiplier",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.company_equity_multiplier for data in statement],
                },
                {
                    "title": "EV multiple",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.ev_multiple for data in statement],
                },
            ],
        }

    @staticmethod
    def operation_risks_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Cobertura de activos",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.asset_coverage_ratio for data in statement],
                },
                {
                    "title": "Cobertuda de flujo de caja",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_flow_coverage_ratios for data in statement],
                },
                {
                    "title": "Cobertuda de efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_coverage for data in statement],
                },
                {
                    "title": "Tasa de cobertura del servicio de la deuda",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.debt_service_coverage for data in statement],
                },
                {
                    "title": "Cobertura de intereses",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.interest_coverage for data in statement],
                },
                {
                    "title": "Ratio cashflow operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.operating_cashflow_ratio for data in statement],
                },
                {
                    "title": "Ratio de deuda",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.debt_ratio for data in statement],
                },
                {
                    "title": "Deuda largo plazo a capitalización",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.long_term_debt_to_capitalization for data in statement],
                },
                {
                    "title": "Deuda total a capitalización",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.total_debt_to_capitalization for data in statement],
                },
            ],
        }

    @staticmethod
    def non_gaap_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Ingresos normalizados",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.normalized_income for data in statement],
                },
                {
                    "title": "Tasa de impuestos",
                    "url": "#!",
                    "percent": "true",
                    "short": "false",
                    "values": [data.effective_tax_rate for data in statement],
                },
                {
                    "title": "NOPAT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.nopat for data in statement],
                },
                {
                    "title": "Net Working capital",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_working_cap for data in statement],
                },
                {
                    "title": "Inventario promedio",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.average_inventory for data in statement],
                },
                {
                    "title": "Promedio cuentas por pagar",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.average_accounts_payable for data in statement],
                },
                {
                    "title": "Dividend yield",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.dividend_yield for data in statement],
                },
                {
                    "title": "Earnings yield",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.earnings_yield for data in statement],
                },
                {
                    "title": "FCF yield",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.fcf_yield for data in statement],
                },
                {
                    "title": "Calidad de los ingresos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.income_quality for data in statement],
                },
                {
                    "title": "Capital invertido",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.invested_capital for data in statement],
                },
                {
                    "title": "Capitalización bursátil",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.market_cap for data in statement],
                },
                {
                    "title": "Valor de los activos corrientes netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.net_current_asset_value for data in statement],
                },
                {
                    "title": "Payout ratio",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.payout_ratio for data in statement],
                },
                {
                    "title": "Valor activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.tangible_assets for data in statement],
                },
                {
                    "title": "Retention ratio",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.retention_ratio for data in statement],
                },
            ],
        }

    @staticmethod
    def per_share_values_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Ventas por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.sales_ps for data in statement],
                },
                {
                    "title": "Activos totales por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.book_ps for data in statement],
                },
                {
                    "title": "Valor tangible por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.tangible_ps for data in statement],
                },
                {
                    "title": "FCF por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.fcf_ps for data in statement],
                },
                {
                    "title": "Beneficio por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.eps for data in statement],
                },
                {
                    "title": "Efectivo por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_ps for data in statement],
                },
                {
                    "title": "Flujo efectivo operativo por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.operating_cf_ps for data in statement],
                },
                {
                    "title": "CAPEX por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.capex_ps for data in statement],
                },
                {
                    "title": "Activos totales por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.total_assets_ps for data in statement],
                },
            ],
        }

    @staticmethod
    def fcf_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "FCF to equity",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.fcf_equity for data in statement],
                },
                {
                    "title": "Unlevered FCF",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.unlevered_fcf for data in statement],
                },
                {
                    "title": "Unlevered FCF EBIT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.unlevered_fcf_ebit for data in statement],
                },
                {
                    "title": "Owners Earnings",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [data.owners_earnings for data in statement],
                },
            ],
        }

    @staticmethod
    def margins_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Margen bruto",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.gross_margin for data in statement],
                },
                {
                    "title": "Margen EBITDA",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.ebitda_margin for data in statement],
                },
                {
                    "title": "Margen Beneficio neto",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.net_income_margin for data in statement],
                },
                {
                    "title": "FCF equidad",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.fcf_equity_to_net_income for data in statement],
                },
                {
                    "title": "Unlevered FCF",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.unlevered_fcf_to_net_income for data in statement],
                },
                {
                    "title": "Unlevered FCF EBIT to Net Income",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.unlevered_fcf_ebit_to_net_income for data in statement],
                },
                {
                    "title": "Owners Earnings to Net Income",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.owners_earnings_to_net_income for data in statement],
                },
                {
                    "title": "Margen flujo de efectivo",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.fcf_margin for data in statement],
                },
            ],
        }

    @staticmethod
    def liquidity_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Cash Ratio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.cash_ratio for data in statement],
                },
                {
                    "title": "Current Ratio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.current_ratio for data in statement],
                },
                {
                    "title": "Quick Ratio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.quick_ratio for data in statement],
                },
                {
                    "title": "Operating cashflow Ratio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.operating_cashflow_ratio for data in statement],
                },
                {
                    "title": "Deuda frente equidad",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.debt_to_equity for data in statement],
                },
            ],
        }

    @staticmethod
    def rentability_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "ROA",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.roa for data in statement],
                },
                {
                    "title": "ROE",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.roe for data in statement],
                },
                {
                    "title": "ROC",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.roc for data in statement],
                },
                {
                    "title": "ROCE",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.roce for data in statement],
                },
                {
                    "title": "ROTA",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.rota for data in statement],
                },
                {
                    "title": "ROIC",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.roic for data in statement],
                },
                {
                    "title": "NOPAT ROIC",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.nopat_roic for data in statement],
                },
                {
                    "title": "ROGIC",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.rogic for data in statement],
                },
            ],
        }

    @staticmethod
    def growth_rates_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Crecimiento de los ingresos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.revenue_growth for data in statement],
                },
                {
                    "title": "Crecimiento de los costos de venta",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.cost_revenue_growth for data in statement],
                },
                {
                    "title": "Crecimiento de los gastos operativos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.operating_expenses_growth for data in statement],
                },
                {
                    "title": "Crecimiento del beneficio neto",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.net_income_growth for data in statement],
                },
                {
                    "title": "Recompara de acciones",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.shares_buyback for data in statement],
                },
                {
                    "title": "Crecimiento del BPA",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.eps_growth for data in statement],
                },
                {
                    "title": "Crecimiento de los ingresos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.fcf_growth for data in statement],
                },
                {
                    "title": "Crecimiento de los owners earnings",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.owners_earnings_growth for data in statement],
                },
                {
                    "title": "Crecimiento del CAPEX",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.capex_growth for data in statement],
                },
                {
                    "title": "Crecimiento del I+D",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [data.rd_expenses_growth for data in statement],
                },
            ],
        }

    @staticmethod
    def price_to_ratios_json(statement: QuerySet):
        return {
            "labels": [data.date_year for data in statement],
            "fields": [
                {
                    "title": "Precio valor en libros",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_book for data in statement],
                },
                {
                    "title": "Precio cashflow",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_cf for data in statement],
                },
                {
                    "title": "Precio beneficio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_earnings for data in statement],
                },
                {
                    "title": "PEG",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_earnings_growth for data in statement],
                },
                {
                    "title": "Precio por ventas",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_sales for data in statement],
                },
                {
                    "title": "Precio activos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_total_assets for data in statement],
                },
                {
                    "title": "Precio FCF",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_fcf for data in statement],
                },
                {
                    "title": "Precio cashflow operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_operating_cf for data in statement],
                },
                {
                    "title": "Precio activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [data.price_tangible_assets for data in statement],
                },
            ],
        }
