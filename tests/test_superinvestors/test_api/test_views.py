import json

from unittest import skip

from bfet import DjangoTestingModel

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


from tests.utils import BaseAPIViewTestMixin
from apps.super_investors.models import Superinvestor
from tests.data.superinvestors.superinvestors_data import LIST_SUPERINVESTORS, SINGLE_SUPERINVESTOR

User = get_user_model()


class TestAllSuperinvestorsAPIView(BaseAPIViewTestMixin, APITestCase):
    path_name = "api:superinvestors_lista_superinversores"
    url_path = "/lista-superinversores/"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        for investor in LIST_SUPERINVESTORS:
            DjangoTestingModel.create(Superinvestor, **investor)

    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = [
            {
                "name": "Bryan Lawrence - Oakcliff Capital",
                "info_accronym": "OCL",
                "slug": "bryan-lawrence-oakcliff-capital",
            },
            {
                "name": "Charlie Munger - Daily Journal Corp.",
                "info_accronym": "DJCO",
                "slug": "charlie-munger-daily-journal-corp",
            },
            {
                "name": "Dennis Hong - ShawSpring Partners",
                "info_accronym": "SP",
                "slug": "dennis-hong-shawspring-partners",
            },
        ]
        assert json.loads(json.dumps(response.data)) == expected_data


class TestSuperinvestorActivityAPIView(BaseAPIViewTestMixin, APITestCase):
    path_name = "api:superinvestors_lista_movimientos"
    url_path = "/lista-movimientos/"
    params = {"slug": ""}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        DjangoTestingModel.create(Superinvestor, **SINGLE_SUPERINVESTOR)

    @skip("Not ready")
    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = []
        assert json.loads(json.dumps(response.data))[0] == expected_data


class TestSuperinvestorHistoryAPIView(BaseAPIViewTestMixin, APITestCase):
    path_name = "api:superinvestors_lista_historial"
    url_path = "/lista-historial/"
    params = {"slug": ""}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    @skip("Not ready")
    def test_success_response(self):
        response = self.client.get(self.full_endpoint, format="json")
        expected_data = []
        assert json.loads(json.dumps(response.data))[0] == expected_data
