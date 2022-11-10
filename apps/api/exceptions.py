from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework import status

from apps.api.constants import WRONG_API_KEY, API_KEY_REMOVED, API_KEY_NOT_FOUND


class AuthenticationFailed(APIException):
    """
    Own AuthenticationFailed created because the one from DRF returns status_code 403
    """
    status_code: int = status.HTTP_401_UNAUTHORIZED
    default_detail: str = ""
    default_code: str = 'authentication_failed'


class KeyRemovedException(PermissionDenied):
    default_detail = API_KEY_REMOVED


class WrongKeyException(AuthenticationFailed):
    default_detail = WRONG_API_KEY


class KeyNotFoundException(AuthenticationFailed):
    default_detail = API_KEY_NOT_FOUND
