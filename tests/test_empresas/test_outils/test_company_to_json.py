from unittest.mock import patch

from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import BalanceSheet, CashflowStatement, Company, IncomeStatement
from src.empresas.outils.company_to_json import CompanyValueToJsonConverter
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.update import UpdateCompany
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from tests.data.empresas import balance_sheets_final_statment, cashflow_final_statment, income_final_statment


class TestCompanyValueToJsonConverter(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.current_period = DjangoTestingModel.create(Period, year=2021, period=PERIOD_FOR_YEAR)
        cls.previous_period = DjangoTestingModel.create(Period, year=2020, period=PERIOD_FOR_YEAR)
        cls.company = DjangoTestingModel.create(Company)
        cls.current_income = DjangoTestingModel.create(
            IncomeStatement,
            period=cls.current_period,
            company=cls.company,
            **income_final_statment.CURRENT_YEAR,
        )
        cls.current_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=cls.current_period,
            company=cls.company,
            **balance_sheets_final_statment.CURRENT_YEAR,
        )
        cls.current_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=cls.current_period,
            company=cls.company,
            **cashflow_final_statment.CURRENT_YEAR,
        )
        cls.previous_income = DjangoTestingModel.create(
            IncomeStatement,
            period=cls.previous_period,
            company=cls.company,
            **income_final_statment.PAST_YEAR,
        )
        cls.previous_balance = DjangoTestingModel.create(
            BalanceSheet,
            period=cls.previous_period,
            company=cls.company,
            **balance_sheets_final_statment.PAST_YEAR,
        )
        cls.previous_cashflow = DjangoTestingModel.create(
            CashflowStatement,
            period=cls.previous_period,
            company=cls.company,
            **cashflow_final_statment.PAST_YEAR,
        )
        all_ratios = CalculateFinancialRatios.calculate_all_ratios(
            cls.company.inc_statements.filter(period=cls.current_period).values(),
            cls.company.balance_sheets.filter(period=cls.current_period).values(),
            cls.company.cf_statements.filter(period=cls.current_period).values(),
            cls.company.inc_statements.filter(period=cls.previous_period).values(),
            cls.company.balance_sheets.filter(period=cls.previous_period).values(),
            cls.company.cf_statements.filter(period=cls.previous_period).values(),
            {"current_price": 34.65},
        )
        UpdateCompany(cls.company).create_or_update_all_ratios(all_ratios, cls.current_period)

    @patch("src.empresas.outils.company_to_json.CompanyValueToJsonConverter.get_currency")
    def test_income_json(self, mock_get_currency):
        mock_get_currency.return_value = "$"
        result = CompanyValueToJsonConverter().income_json(self.company.inc_statements.all())
        assert result == {
            "currency": "$",
            "labels": ["2021", "2020"],
            "fields": [
                {
                    "title": "Ingresos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [365817000000.0, 274515000000.0],
                },
                {
                    "title": "Costos de venta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [212981000000.0, 169559000000.0],
                },
                {
                    "title": "Utilidad bruta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [152836000000.0, 104956000000.0],
                },
                {"title": "I&D", "url": "#!", "percent": "false", "short": "false", "values": [0.0, 0.0]},
                {
                    "title": "Gastos administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Gastos marketing",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [21973000000.0, 19916000000.0],
                },
                {
                    "title": "Gastos marketing, generales y administrativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-258000000.0, -803000000.0],
                },
                {
                    "title": "Gastos otros",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [21914000000.0, 18752000000.0],
                },
                {
                    "title": "Gastos operativos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [108949000000.0, 66288000000.0],
                },
                {
                    "title": "Gastos y costos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [256868000000.0, 208227000000.0],
                },
                {
                    "title": "Intereses",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [2645000000.0, 2873000000.0],
                },
                {
                    "title": "Depreciación & Amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [11284000000.0, 11056000000.0],
                },
                {
                    "title": "EBITDA",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [123136000000.0, 81020000000.0],
                },
                {
                    "title": "Ingresos de explotación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Otros Gastos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [43887000000.0, 38668000000.0],
                },
                {
                    "title": "EBT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [109207000000.0, 67091000000.0],
                },
                {
                    "title": "Impuestos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [14527000000.0, 9680000000.0],
                },
                {
                    "title": "Ingresos netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [94680000000.0, 57411000000.0],
                },
                {
                    "title": "Acciones en circulación",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [16864919000.0, 17528214000.0],
                },
                {
                    "title": "Acciones diluidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [16701272000.0, 17352119000.0],
                },
            ],
        }

    @patch("src.empresas.outils.company_to_json.CompanyValueToJsonConverter.get_currency")
    def test_balance_json(self, mock_get_currency):
        mock_get_currency.return_value = "$"
        result = CompanyValueToJsonConverter().balance_json(self.company.balance_sheets.all())
        assert result == {
            "currency": "$",
            "labels": ["2021", "2020"],
            "fields": [
                {
                    "title": "Efectivo y equivalentes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [34940000000.0, 38016000000.0],
                },
                {
                    "title": "Inversiones corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [27699000000.0, 52927000000.0],
                },
                {
                    "title": "Efectivo e inversiones corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [62639000000.0, 90943000000.0],
                },
                {
                    "title": "Cuentas por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [51506000000.0, 37445000000.0],
                },
                {
                    "title": "Inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [6580000000.0, 4061000000.0],
                },
                {
                    "title": "Otro activos corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [14111000000.0, 11264000000.0],
                },
                {
                    "title": "Activos corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [134836000000.0, 143713000000.0],
                },
                {
                    "title": "Propiedades y equipamiento",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [39440000000.0, 36766000000.0],
                },
                {"title": "Goodwill", "url": "#!", "percent": "false", "short": "false", "values": [0.0, 0.0]},
                {
                    "title": "Activos intangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Goodwill y activos intangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Inversiones a largo plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [127877000000.0, 100887000000.0],
                },
                {
                    "title": "Impuestos retenidos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Otros activos no corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [48849000000.0, 42522000000.0],
                },
                {
                    "title": "Activos no corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [216166000000.0, 180175000000.0],
                },
                {"title": "Otros activos", "url": "#!", "percent": "false", "short": "false", "values": [0.0, 0.0]},
                {
                    "title": "Activos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [351002000000.0, 323888000000.0],
                },
                {
                    "title": "Cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [54763000000.0, 42296000000.0],
                },
                {
                    "title": "Deuda a corto plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [15613000000.0, 13769000000.0],
                },
                {
                    "title": "Impuestos por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Ingreso diferido",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [7612000000.0, 6643000000.0],
                },
                {
                    "title": "Otros pasivos corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [47493000000.0, 42684000000.0],
                },
                {
                    "title": "Pasivos corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [125481000000.0, 105392000000.0],
                },
                {
                    "title": "Deuda a largo plazo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [109106000000.0, 98667000000.0],
                },
                {
                    "title": "Otros ingresos por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Otros impuestos por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Otros pasivos no corrientes",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [53325000000.0, 54490000000.0],
                },
                {
                    "title": "Pasivos no corrientes totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [162431000000.0, 153157000000.0],
                },
                {"title": "Otros pasivos", "url": "#!", "percent": "false", "short": "false", "values": [0.0, 0.0]},
                {
                    "title": "Pasivos totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [287912000000.0, 258549000000.0],
                },
                {
                    "title": "Ingresos para accionistas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [57365000000.0, 50779000000.0],
                },
                {
                    "title": "Ganancias retenidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [5562000000.0, 14966000000.0],
                },
                {
                    "title": "Otras pérdidas acumuladas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [163000000.0, -406000000.0],
                },
                {
                    "title": "Otra equidad total",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Equidad de los accionistas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [63090000000.0, 65339000000.0],
                },
                {
                    "title": "Equidad y deuda totalas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [351002000000.0, 323888000000.0],
                },
                {
                    "title": "Inversiones totales",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [155576000000.0, 153814000000.0],
                },
                {
                    "title": "Deuda total",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [124719000000.0, 112436000000.0],
                },
                {
                    "title": "Deuda neta",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [89779000000.0, 74420000000.0],
                },
            ],
        }

    @patch("src.empresas.outils.company_to_json.CompanyValueToJsonConverter.get_currency")
    def test_cashflow_json(self, mock_get_currency):
        mock_get_currency.return_value = "$"
        result = CompanyValueToJsonConverter().cashflow_json(self.company.cf_statements.all())
        assert result == {
            "currency": "$",
            "labels": ["2021", "2020"],
            "fields": [
                {
                    "title": "Beneficio neto",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-93353000000.0, -10435000000.0],
                },
                {
                    "title": "Depreciación y amortización",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [11284000000.0, 11056000000.0],
                },
                {
                    "title": "Impuesto sobre beneficio diferido",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-4774000000.0, -215000000.0],
                },
                {
                    "title": "Compensación en acciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [7906000000.0, 6829000000.0],
                },
                {
                    "title": "Cambios en working capital",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-4911000000.0, 5690000000.0],
                },
                {
                    "title": "Cuentas por cobrar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-10125000000.0, 6917000000.0],
                },
                {
                    "title": "Inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-2642000000.0, -127000000.0],
                },
                {
                    "title": "Cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [12326000000.0, -4062000000.0],
                },
                {
                    "title": "Otro working capital",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [1676000000.0, 2081000000.0],
                },
                {
                    "title": "Otras utilidades no en efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-147000000.0, -97000000.0],
                },
                {
                    "title": "Flujo de caja de las operaciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [94680000000.0, 57411000000.0],
                },
                {
                    "title": "Inversiones en plantas y equipamiento",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-14545000000.0, -4289000000.0],
                },
                {
                    "title": "Adquisiciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-33000000.0, -1524000000.0],
                },
                {
                    "title": "Inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-109689000000.0, -115148000000.0],
                },
                {
                    "title": "Ingresos por venta de inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [106870000000.0, 120483000000.0],
                },
                {
                    "title": "Otras inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-608000000.0, -791000000.0],
                },
                {
                    "title": "Flujo de caja dedicado a inversiones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [104038000000.0, 80674000000.0],
                },
                {
                    "title": "Pago de deudas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-8750000000.0, -12629000000.0],
                },
                {
                    "title": "Acciones emitidas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [1105000000.0, 880000000.0],
                },
                {
                    "title": "Recompra de acciones",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-85971000000.0, -72358000000.0],
                },
                {
                    "title": "Dividendos pagados",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-14467000000.0, -14081000000.0],
                },
                {
                    "title": "Otras actividades financieras",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-6685000000.0, 11368000000.0],
                },
                {
                    "title": "Flujo de caja usado (proporcionado) por actividades financieras",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-11085000000.0, -7309000000.0],
                },
                {
                    "title": "Efecto del cambio de divisas",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0, 0.0],
                },
                {
                    "title": "Cambio en efectivo neto",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-93353000000.0, -86820000000.0],
                },
                {
                    "title": "Efectivo al final del periodo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [35929000000.0, 39789000000.0],
                },
                {
                    "title": "Efectivo al principio del periodo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [39789000000.0, 50224000000.0],
                },
                {
                    "title": "Flujo de caja operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [104038000000.0, 80674000000.0],
                },
                {
                    "title": "CAPEX",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-11085000000.0, -7309000000.0],
                },
                {
                    "title": "Flujo de caja libre",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [92953000000.0, 73365000000.0],
                },
            ],
        }

    def test_efficiency_ratios_json(self):
        result = CompanyValueToJsonConverter.efficiency_ratios_json(self.company.efficiency_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Rotación de activos", "url": "#!", "percent": "false", "short": "true", "values": [1.084]},
                {
                    "title": "Rotación del inventario",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-153.832],
                },
                {
                    "title": "Rotación de activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {
                    "title": "Rotación de cuentas por pagar",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [2.983],
                },
                {
                    "title": "Ciclo conversión de efectivo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-299.66499999999996],
                },
                {
                    "title": "Inventario disponible (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {
                    "title": "Cuentas por pagar en circulación (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {
                    "title": "Ventas activas (Días)",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-299.66499999999996],
                },
                {
                    "title": "Ratio FCF a flujo de efectivo operativo",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "Ciclo operativo", "url": "#!", "percent": "false", "short": "true", "values": [-299.66]},
            ],
        }

    def test_ev_ratios_json(self):
        result = CompanyValueToJsonConverter.ev_ratios_json(self.company.ev_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {
                    "title": "Capitalización bursátil",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [0.0],
                },
                {
                    "title": "Enterprise value",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [62080000000.0],
                },
                {"title": "EV to free cash flow", "url": "#!", "percent": "false", "short": "true", "values": [0.0]},
                {
                    "title": "EV to operating cashflow",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "EV to sales", "url": "#!", "percent": "false", "short": "true", "values": [0.17]},
                {"title": "Equity multiplier", "url": "#!", "percent": "false", "short": "true", "values": [5.56]},
                {"title": "EV multiple", "url": "#!", "percent": "false", "short": "true", "values": [0.5]},
            ],
        }

    def test_operation_risks_ratios_json(self):
        result = CompanyValueToJsonConverter.operation_risks_ratios_json(self.company.operation_risks_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Cobertura de activos", "url": "#!", "percent": "false", "short": "true", "values": [79.36]},
                {
                    "title": "Cobertuda de flujo de caja",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "Cobertuda de efectivo", "url": "#!", "percent": "false", "short": "true", "values": [23.68]},
                {
                    "title": "Tasa de cobertura del servicio de la deuda",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "Cobertura de intereses", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
                {
                    "title": "Ratio cashflow operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "Ratio de deuda", "url": "#!", "percent": "false", "short": "true", "values": [0.36]},
                {
                    "title": "Deuda largo plazo a capitalización",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [1.0],
                },
                {
                    "title": "Deuda total a capitalización",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.66],
                },
            ],
        }

    def test_non_gaap_json(self):
        result = CompanyValueToJsonConverter.non_gaap_json(self.company.non_gaap_figures.all())
        assert result == {
            "labels": [],
            "fields": [
                {"title": "Ingresos normalizados", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Tasa de impuestos", "url": "#!", "percent": "true", "short": "false", "values": []},
                {"title": "NOPAT", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Net Working capital", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Inventario promedio", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "Promedio cuentas por pagar", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "Dividend yield", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "Earnings yield", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "FCF yield", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "Calidad de los ingresos", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Capital invertido", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Capitalización bursátil", "url": "#!", "percent": "false", "short": "false", "values": []},
                {
                    "title": "Valor de los activos corrientes netos",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [],
                },
                {"title": "Payout ratio", "url": "#!", "percent": "true", "short": "true", "values": []},
                {"title": "Valor activos tangibles", "url": "#!", "percent": "false", "short": "false", "values": []},
                {"title": "Retention ratio", "url": "#!", "percent": "true", "short": "true", "values": []},
            ],
        }

    def test_per_share_values_json(self):
        result = CompanyValueToJsonConverter.per_share_values_json(self.company.per_share_values.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Ventas por acción", "url": "#!", "percent": "false", "short": "true", "values": [21.691]},
                {
                    "title": "Activos totales por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [3.7409],
                },
                {
                    "title": "Valor tangible por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-9.0766],
                },
                {"title": "FCF por acción", "url": "#!", "percent": "false", "short": "true", "values": [0.0]},
                {
                    "title": "Beneficio por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-5.5353],
                },
                {"title": "Efectivo por acción", "url": "#!", "percent": "false", "short": "true", "values": [3.7142]},
                {
                    "title": "Flujo efectivo operativo por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "CAPEX por acción", "url": "#!", "percent": "false", "short": "true", "values": [0.0]},
                {
                    "title": "Activos totales por acción",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [20.8126],
                },
            ],
        }

    def test_fcf_ratios_json(self):
        result = CompanyValueToJsonConverter.fcf_ratios_json(self.company.fcf_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {
                    "title": "FCF to equity",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-8750000000.0],
                },
                {
                    "title": "Unlevered FCF",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-239750000000.0],
                },
                {
                    "title": "Unlevered FCF EBIT",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-244524000000.0],
                },
                {
                    "title": "Owners Earnings",
                    "url": "#!",
                    "percent": "false",
                    "short": "false",
                    "values": [-333103000000.0],
                },
            ],
        }

    def test_margins_json(self):
        result = CompanyValueToJsonConverter.margins_json(self.company.margins.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Margen bruto", "url": "#!", "percent": "true", "short": "true", "values": [42.0]},
                {"title": "Margen EBITDA", "url": "#!", "percent": "true", "short": "true", "values": [34.0]},
                {"title": "Margen Beneficio neto", "url": "#!", "percent": "true", "short": "true", "values": [-26.0]},
                {"title": "FCF equidad", "url": "#!", "percent": "true", "short": "true", "values": [9.0]},
                {"title": "Unlevered FCF", "url": "#!", "percent": "true", "short": "true", "values": [257.0]},
                {
                    "title": "Unlevered FCF EBIT to Net Income",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [262.0],
                },
                {
                    "title": "Owners Earnings to Net Income",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [357.0],
                },
                {"title": "Margen flujo de efectivo", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
            ],
        }

    def test_liquidity_ratios_json(self):
        result = CompanyValueToJsonConverter.liquidity_ratios_json(self.company.liquidity_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Cash Ratio", "url": "#!", "percent": "false", "short": "true", "values": [0.28]},
                {"title": "Current Ratio", "url": "#!", "percent": "false", "short": "true", "values": [1.07]},
                {"title": "Quick Ratio", "url": "#!", "percent": "false", "short": "true", "values": [0.91]},
                {
                    "title": "Operating cashflow Ratio",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {"title": "Deuda frente equidad", "url": "#!", "percent": "false", "short": "true", "values": [4.56]},
            ],
        }

    def test_rentability_ratios_json(self):
        result = CompanyValueToJsonConverter.rentability_ratios_json(self.company.rentability_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "ROA", "url": "#!", "percent": "true", "short": "true", "values": [-27.0]},
                {"title": "ROE", "url": "#!", "percent": "true", "short": "true", "values": [-148.0]},
                {"title": "ROC", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
                {"title": "ROCE", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
                {"title": "ROTA", "url": "#!", "percent": "true", "short": "true", "values": [-69.0]},
                {"title": "ROIC", "url": "#!", "percent": "true", "short": "true", "values": [-178.0]},
                {"title": "NOPAT ROIC", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
                {"title": "ROGIC", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
            ],
        }

    def test_growth_rates_json(self):
        result = CompanyValueToJsonConverter.growth_rates_json(self.company.growth_rates.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {
                    "title": "Crecimiento de los ingresos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [33.0],
                },
                {
                    "title": "Crecimiento de los costos de venta",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [26.0],
                },
                {
                    "title": "Crecimiento de los gastos operativos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [23.0],
                },
                {
                    "title": "Crecimiento del beneficio neto",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [795.0],
                },
                {"title": "Recompara de acciones", "url": "#!", "percent": "true", "short": "true", "values": [-4.0]},
                {"title": "Crecimiento del BPA", "url": "#!", "percent": "true", "short": "true", "values": [830.0]},
                {
                    "title": "Crecimiento de los ingresos",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [0.0],
                },
                {
                    "title": "Crecimiento de los owners earnings",
                    "url": "#!",
                    "percent": "true",
                    "short": "true",
                    "values": [6920.0],
                },
                {"title": "Crecimiento del CAPEX", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
                {"title": "Crecimiento del I+D", "url": "#!", "percent": "true", "short": "true", "values": [0.0]},
            ],
        }

    def test_price_to_ratios_json(self):
        result = CompanyValueToJsonConverter.price_to_ratios_json(self.company.price_to_ratios.all())
        assert result == {
            "labels": ["2021"],
            "fields": [
                {"title": "Precio valor en libros", "url": "#!", "percent": "false", "short": "true", "values": [9.26]},
                {"title": "Precio cashflow", "url": "#!", "percent": "false", "short": "true", "values": [9.33]},
                {"title": "Precio beneficio", "url": "#!", "percent": "false", "short": "true", "values": [-6.26]},
                {"title": "PEG", "url": "#!", "percent": "false", "short": "true", "values": [-0.01]},
                {"title": "Precio por ventas", "url": "#!", "percent": "false", "short": "true", "values": [1.6]},
                {"title": "Precio activos totales", "url": "#!", "percent": "false", "short": "true", "values": [1.66]},
                {"title": "Precio FCF", "url": "#!", "percent": "false", "short": "true", "values": [0.0]},
                {
                    "title": "Precio cashflow operativo",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [0.0],
                },
                {
                    "title": "Precio activos tangibles",
                    "url": "#!",
                    "percent": "false",
                    "short": "true",
                    "values": [-3.82],
                },
            ],
        }
