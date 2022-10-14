import json

from apps.api.mixins import BaseAPIViewTest


class TestAllSuperinvestorsAPIView(BaseAPIViewTest):
    path_name = "api:superinvestors_lista_superinversores"
    url_path = "/lista-superinversores/"

    def test_success_response(self, client, various_terms):
        response = client.get(self.full_endpoint, format="json")
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
        assert json.loads(json.dumps(response.data))[0] == expected_data


from django.test import TestCase


class TestSuperinvestorActivityAPIView(BaseAPIViewTest):
    path_name = "api:superinvestors_lista_movimientos"
    url_path = "/lista-movimientos/"
    params = {"slug": ""}

    def test_success_response(self, client, various_terms):
        response = client.get(self.full_endpoint, format="json")
        expected_data = []
        assert json.loads(json.dumps(response.data))[0] == expected_data


from django.test import TestCase


class TestSuperinvestorHistoryAPIView(BaseAPIViewTest):
    path_name = "api:superinvestors_lista_historial"
    url_path = "/lista-historial/"
    params = {"slug": ""}

    def test_success_response(self, client, various_terms):
        response = client.get(self.full_endpoint, format="json")
        expected_data = []
        assert json.loads(json.dumps(response.data))[0] == expected_data
