from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from src.api.constants import HTTP_AUTH_HEADER
from src.api.exceptions import (
    JWTErrorException,
    JWTInvalidException,
    JWTIWithoutUserException,
    JWTUserNotMatchUserException,
    KeyNotFoundException,
    KeyRemovedException,
    WrongKeyException,
)
from src.api.facade import JwtFacade, JWTPayload
from src.api.models import Jwt, Key
from src.users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[User, Jwt]:
        raw_token = self.get_authorization_header(request)
        payload = self.get_payload(raw_token)
        user, token = self.get_user(payload), self.get_token(payload)
        if user != token.user:
            raise JWTUserNotMatchUserException()
        return user, token

    def get_authorization_header(self, request: Request) -> str:
        return request.META.get(HTTP_AUTH_HEADER, "").replace("Bearer ", "")

    def get_payload(self, token: str) -> JWTPayload:
        try:
            return JwtFacade.decode(token)
        except Exception as e:
            raise JWTErrorException(e) from e

    def get_token(self, payload: JWTPayload) -> Jwt:
        try:
            return Jwt.objects.get(pk=payload.jti)
        except Jwt.DoesNotExist as e:
            raise JWTInvalidException() from e

    def get_user(self, payload: JWTPayload) -> User:
        try:
            return User.objects.get(pk=payload.sub)
        except User.DoesNotExist as e:
            raise JWTIWithoutUserException() from e


class KeyAuthentication(BaseAuthentication):
    # TODO: rename key for token
    def authenticate(self, request: Request) -> tuple[User, Key]:
        key_param = self.get_authorization_params(request)
        token = self.get_token(key_param)
        user = self.get_user(token)
        return user, token

    def get_authorization_params(self, request: Request) -> str:
        if token := request.GET.get("api_key"):
            return token
        raise KeyNotFoundException()

    def get_token(self, token: str) -> Key:
        try:
            return Key.objects.get(key=token)
        except Key.DoesNotExist as e:
            raise WrongKeyException() from e

    def get_user(self, token: Key) -> User:
        if token.in_use:
            # DRF wants to receive (request.user, request.auth)
            # https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
            return token.user
        else:
            raise KeyRemovedException()
