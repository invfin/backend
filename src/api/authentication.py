from typing import Tuple

from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication

from src.api.exceptions import KeyNotFoundException, KeyRemovedException, WrongKeyException
from src.api.models import Key

User = get_user_model()


class KeyAuthentication(BaseAuthentication):
    def get_key_from_params(self, request) -> str:
        key = request.GET.get("api_key")
        if key:
            return key
        raise KeyNotFoundException()

    def check_key_exists(self, key: str) -> Key:
        try:
            key_obj = Key.objects.get(key=key)
        except Key.DoesNotExist:
            raise WrongKeyException()
        else:
            return key_obj

    def check_key_is_use(self, key: Key) -> Tuple[User, Key]:
        if key.in_use:
            # DRF wants to receive (request.user, request.auth)
            # https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
            return key.user, key
        else:
            raise KeyRemovedException()

    def authenticate(self, request):
        key = self.get_key_from_params(request)
        key_obj = self.check_key_exists(key)
        return self.check_key_is_use(key_obj)
