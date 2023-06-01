from unittest.mock import patch, call

from django.test import TestCase

from src.empresas.outils.data_management.interfaces import CompanyInterface
from src.empresas.outils.data_management.show.chart_presentation import (
    CompanyChartPresentation,
)

EMPRESA_DATA_MNGMT = "src.empresas.outils.data_management"

COMPANY_DATA = f"{EMPRESA_DATA_MNGMT}.show.company_data.CompanyData"
PRESENTATION = f"{EMPRESA_DATA_MNGMT}.show.chart_presentation.CompanyChartPresentation"


class TestCompanyChartPresentation(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = CompanyInterface()()
        cls.presentation = CompanyChartPresentation()

    @patch(
        f"{PRESENTATION}.build_table_and_chart",
        side_effect=[
            "comparing_income_json",
            "comparing_balance_json",
            "comparing_cashflows",
        ],
    )
    @patch(f"{PRESENTATION}.get_important_ratios")
    @patch(f"{PRESENTATION}.get_secondary_ratios")
    def test_get_complete_information(
        self,
        mock_get_secondary_ratios,
        mock_get_important_ratios,
        mock_build_table_and_chart,
    ):
        comparing_income_json = self.build_table_and_chart(
            initial_statements.inc_statements,
            self.income_json,
        )
        comparing_balance_json = self.build_table_and_chart(
            initial_statements.balance_sheets,
            self.balance_json,
        )
        comparing_cashflows = self.build_table_and_chart(
            initial_statements.cf_statements,
            self.cashflow_json,
        )
        self.assertEqual(
            self.presentation.get_complete_information(),
            {
                "comparing_income_json": "comparing_income_json",
                "comparing_balance_json": "comparing_balance_json",
                "comparing_cashflows": "comparing_cashflows",
                "important_ratios": self.get_important_ratios(initial_statements),
                "secondary_ratios": self.get_secondary_ratios(initial_statements),
            },
        )
        self.assertEqual(
            mock_build_table_and_chart.call_args_list,
            [
                call(self.presentation.income_json),
            ],
        )

    def test_compare_most_used_ratios(self):
        self.assertEqual(
            self.presentation.compare_most_used_ratios(),
            [],
        )

    def test_to_size_ratios(self):
        self.assertEqual(
            self.presentation.to_size_ratios(),
            [],
        )

    @patch(f"{PRESENTATION}.build_table_and_chart")
    def test_get_important_ratios(self):
        self.assertEqual(
            self.presentation.get_important_ratios(),
            [],
        )

    @patch(f"{PRESENTATION}.build_table_and_chart")
    def test_get_secondary_ratios(self):
        call()
        self.assertEqual(
            self.presentation.get_secondary_ratios(),
            [],
        )

    def test_generate_limit(self):
        self.assertEqual(
            self.presentation.generate_limit(),
            [],
        )

    @patch("src.empresas.outils.company.CompanyData.income_json")
    @patch("src.general.utils.ChartSerializer.generate_json")
    def test_build_table_and_chart(self, mock_generate_json, mock_income_json):
        mock_generate_json.return_value = "value"
        mock_income_json.return_value = "value"
        statement = self.company.inc_statements.all()
        result = CompanyData(None).build_table_and_chart(
            statement,
            CompanyData.income_json,
        )
        mock_income_json.assert_called_once_with(statement)
        mock_generate_json.assert_called_once_with("value", None, "line")
        self.assertDictEqual(result, {"table": "value", "chart": "value"})
