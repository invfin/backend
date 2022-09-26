from typing import Union, Dict, Any

import urllib

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework import status
from bfet import DjangoTestingModel as DTM

from apps.api.models import Key


HTTP_VERBS = {
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
}


class BaseAPIViewTest(APITestCase):
    """
    Mixin for sharing test methods for views.
    Needs the following attributes:
      - allowed_verbs: containing a set of HTTP verbs that should not return 405,
        check HTTP_VERBS for full list of verbs.
      - endpoint: full url
    """

    allowed_verbs = {"GET", "HEAD", "OPTIONS"}
    path_name: str = ""
    url_path: str = ""
    api_key_param: str = "api_key"
    no_key_error_message: str = (
        "Tu clave es incorrecta, asegúrate que está bien escrita depués de api_key=<clave> o pide tu clave desde tu"
        " perfil"
    )
    params: Dict[str, Any] = {}
    wrong_param_error_message: str = "Ha habido un problema con tu búsqueda, asegúrate de haber introducido un valor"
    no_param_error_messages: str = "No has introducido ninguna búsqueda"
    not_found_error_messages: str = "Tu búsqueda no ha devuelto ningún resultado"
    server_problem_error_message: str = "Lo siento ha habido un problema"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.auth_user = DTM.create(get_user_model())
        cls.user_sub_key = DTM.create(Key, user=cls.auth_user, in_use=True)

        cls.auth_user_2 = DTM.create(get_user_model())
        cls.user_no_sub_key = DTM.create(Key, user=cls.auth_user_2, in_use=True)

        cls.no_auth_user = DTM.create(get_user_model())

        cls.endpoint = reverse(cls.path_name)
        cls.endpoint_key = f"{cls.endpoint}?{cls.api_key_param}={cls.user_sub_key.key}"
        cls.full_endpoint = cls.endpoint_key

        if cls.params:
            params = urllib.parse.urlencode(params)
            cls.full_endpoint = f"{cls.full_endpoint}&{params}"

    def test_verbs(self):
        for verb in self.allowed_verbs:
            with self.subTest(f"Testing {verb}"):
                self.assertNotEqual(
                    self.client.generic(verb, self.endpoint).status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                )

        for verb in HTTP_VERBS - self.allowed_verbs:
            with self.subTest(f"Testing {verb}"):
                self.assertEqual(
                    self.client.generic(verb, self.endpoint).status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                )

    def test_url(self):
        self.assertEqual(self.endpoint, self.url_path)

    def test_no_auth(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(
            response.data, {"detail": ErrorDetail(string=self.no_key_error_message, code="permission_denied")}
        )

    def test_server_problem(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(
            response.data, {"detail": ErrorDetail(string=self.server_problem_error_message, code="permission_denied")}
        )

    def test_no_params(self):
        if self.params:
            response = self.client.get(self.endpoint_key)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertDictEqual(
                response.data, {"detail": ErrorDetail(string=self.no_param_error_messages, code="parse_error")}
            )

    def test_wrong_params(self):
        if self.params:
            for key in self.params.keys():
                with self.subTest(f"Testing param {key}"):
                    params = self.params
                    params[key] = "random"
                    params = urllib.parse.urlencode(params)
                    response = self.client.get(f"{self.endpoint_key}&{params}")
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertDictEqual(
                        response.data,
                        {"detail": ErrorDetail(string=self.wrong_param_error_message, code="parse_error")},
                    )

    def test_success(self):
        response = self.client.get(self.full_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
