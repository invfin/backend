from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext

from bfet import DjangoTestingModel as DTM

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from apps.api.mixins import BaseAPIViewTest
from apps.empresas.models import IncomeStatement, BalanceSheet, CashflowStatement, Company


class TestExcelAPIIncome(BaseAPIViewTest):
    path_name = "empresas:ExcelAPIIncome"
    url_path = "/company-information/excel-api/income"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(IncomeStatement, company=DTM.create(Company, ticker="AAPL"))

    # def test_number_of_queries(self):
    #     with CaptureQueriesContext(connection) as ctx:
    #         self.client.get(self.endpoint)
    #     self.assertEqual(len(ctx), 6)

    def test_success_response(self):
        response = self.client.get(self.full_endpoint)
        print(response)
        self.assertDictEqual(response.data, {})

    def test_not_found(self):
        response = self.client.get(f"{self.endpoint}?")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.data, {"detail": ErrorDetail(string="Not found.", code="not_found")})


class TestExcelAPIBalance(BaseAPIViewTest):
    path_name = "empresas:ExcelAPIBalance"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(BalanceSheet, company=DTM.create(Company, ticker="AAPL"))

    def test_url(self):
        self.assertEqual(self.endpoint, f"company-information/excel-api/balance")


class TestExcelAPICashflow(BaseAPIViewTest):
    path_name = "empresas:ExcelAPICashflow"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.statement = DTM.create(CashflowStatement, company=DTM.create(Company, ticker="AAPL"))

    def test_url(self):
        self.assertEqual(self.endpoint, f"company-information/excel-api/cashflow")
