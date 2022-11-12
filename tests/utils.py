import urllib

import datetime
from typing import Dict, Any
from unittest import skip

from bfet import DjangoTestingModel

from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.exceptions import ErrorDetail, server_error
from rest_framework import status

from apps.api.models import Key
from apps.business.models import (
    Product,
    ProductComplementary,
    ProductSubscriber,
)
from apps.currencies.models import Currency

User = get_user_model()

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


class BaseAPIViewTestMixin:
    """
    Mixin for sharing test methods for views.
    Needs the following attributes:
      - allowed_verbs: containing a set of HTTP verbs that should not return 405,
        check HTTP_VERBS for full list of verbs.
      - endpoint: full url
    """

    api_prefix: str = "api"
    api_version: str = settings.API_VERSION["CURRENT_VERSION"]
    allowed_verbs: set = {"GET", "HEAD", "OPTIONS"}
    path_name: str = ""
    url_path: str = ""
    api_key_param: str = "api_key"
    wrong_key_error_message: str = (
        "Tu clave es incorrecta, asegúrate que está bien escrita depués de api_key=<clave> o pide tu clave desde tu"
        " perfil"
    )
    no_api_key_error_message: str = "Introduce tu clave en api_key, si no tienes alguna entra en tu perfil para crearla"
    api_key_removed: str = "Tu clave ya no es válida, crea una nueva desde tu perfil"
    params: Dict[str, Any] = {}
    wrong_param_error_message: str = (
        "Ha habido un problema con tu búsqueda, asegúrate de haber introducido los parámetros correctamente"
    )
    no_param_error_messages: str = "No has introducido ninguna búsqueda"
    not_found_error_messages: str = "Tu búsqueda no ha devuelto ningún resultado"
    server_problem_error_message: str = "Lo siento hemos tenido un problema, reinténtalo en un momento"
    actual_api: bool = True  # To remove once API for excel is actual url

    @classmethod
    def setUpTestData(cls) -> None:
        user_key_sub = DjangoTestingModel.create(User)
        user_key_removed = DjangoTestingModel.create(User)
        user_key = DjangoTestingModel.create(User)
        product = DjangoTestingModel.create(Product, title="Excel", slug="excel", is_active=True)
        product_complementary = DjangoTestingModel.create(
            ProductComplementary,
            title="Subscripción excel",
            product=product,
            is_active=True,
            currency=DjangoTestingModel.create(Currency),
        )
        product_subscriber = DjangoTestingModel.create(
            ProductSubscriber,
            product=product,
            product_complementary=product_complementary,
            subscriber=user_key_sub,
            is_active=True,
        )
        cls.subscription_key = DjangoTestingModel.create(
            Key, user=user_key_sub, in_use=True, removed=None, subscription=product_subscriber
        )
        cls.removed_key = DjangoTestingModel.create(
            Key, user=user_key_removed, in_use=False, removed=datetime.datetime.utcnow()
        )
        cls.key = DjangoTestingModel.create(Key, user=user_key, in_use=True, removed=None)
        cls.endpoint = resolve_url(cls.path_name)
        cls.endpoint_no_key = f"{cls.endpoint}?{cls.api_key_param}="
        cls.endpoint_removed_key = f"{cls.endpoint_no_key}{cls.removed_key.key}"
        cls.endpoint_wrong_key = f"{cls.endpoint_removed_key}4"
        cls.endpoint_key = f"{cls.endpoint_no_key}{cls.subscription_key.key}"
        cls.full_endpoint = cls.endpoint_key
        if cls.params:
            params = urllib.parse.urlencode(cls.params)
            cls.full_endpoint = f"{cls.full_endpoint}&{params}"

    def test_verbs(self):
        for verb in self.allowed_verbs:
            with self.subTest(f"testing {verb}"):
                assert self.client.generic(verb, self.full_endpoint).status_code != status.HTTP_405_METHOD_NOT_ALLOWED
                assert self.client.generic(verb, self.full_endpoint).status_code == status.HTTP_200_OK

        for verb in HTTP_VERBS - self.allowed_verbs:
            with self.subTest(f"testing {verb}"):
                assert (
                    self.client.generic(verb, self.full_endpoint).status_code == status.HTTP_403_FORBIDDEN
                )  # status.HTTP_405_METHOD_NOT_ALLOWED

    def test_url(self):
        if self.actual_api:
            assert resolve_url(self.path_name) == f"/{self.api_prefix}/{self.api_version}{self.url_path}"
        else:
            assert resolve_url(self.path_name) == f"{self.url_path}"

    def test_no_auth(self):
        for endpoint, endpoint_name, status_code, error_message, error_code in [
            (
                self.endpoint_removed_key,
                "Key removed endpoint",
                status.HTTP_403_FORBIDDEN,
                self.api_key_removed,
                "permission_denied",
            ),
            (
                self.endpoint_wrong_key,
                "Wrong key endpoint",
                status.HTTP_401_UNAUTHORIZED,
                self.wrong_key_error_message,
                "authentication_failed",
            ),
            (
                self.endpoint_no_key,
                "No key endpoint",
                status.HTTP_401_UNAUTHORIZED,
                self.no_api_key_error_message,
                "authentication_failed",
            ),
        ]:
            with self.subTest(endpoint_name):
                if self.params:
                    params = urllib.parse.urlencode(self.params)
                    endpoint = f"{endpoint}&{params}"
                response = self.client.get(endpoint)
                assert response.status_code == status_code
                assert response.data == {"detail": ErrorDetail(string=error_message, code=error_code)}

    @skip("Skipping")
    def test_server_problem(self):
        """
        TODO
        Mock the request to assert en error
        """
        with self.assertRaises(server_error):
            response = self.client.get(self.full_endpoint)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response.data == {
                "detail": ErrorDetail(string=self.server_problem_error_message, code="permission_denied")
            }

    def test_no_params(self):
        if self.params:
            response = self.client.get(self.endpoint_key)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.data == {"detail": ErrorDetail(string=self.no_param_error_messages, code="parse_error")}

    def test_wrong_params(self):
        if self.params:
            original_params = {**self.params}
            for key in self.params.keys():
                with self.subTest(key):
                    params = original_params
                    params["bad"] = params.pop(key)
                    params = urllib.parse.urlencode(params)
                    response = self.client.get(f"{self.endpoint_key}&{params}")
                    assert response.status_code == status.HTTP_400_BAD_REQUEST
                    assert response.data == {
                        "detail": ErrorDetail(string=self.wrong_param_error_message, code="parse_error")
                    }

    def test_not_found(self):
        if self.params:
            original_params = {**self.params}
            for key in self.params.keys():
                with self.subTest(key):
                    params = original_params
                    if key == "id":
                        random_value = 1233425
                    else:
                        random_value = "random"
                    params[key] = random_value
                    params = urllib.parse.urlencode(params)
                    response = self.client.get(f"{self.endpoint_key}&{params}")
                    assert response.status_code == status.HTTP_404_NOT_FOUND
                    assert response.data == {
                        "detail": ErrorDetail(string=self.not_found_error_messages, code="not_found")
                    }

    def test_success(self):
        response = self.client.get(self.full_endpoint)
        assert response.status_code == status.HTTP_200_OK
