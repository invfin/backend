from rest_framework.exceptions import PermissionDenied, APIException, ParseError, NotFound
from rest_framework import status

from apps.api import constants


class ServerError(APIException):
    default_detail = constants.SERVER_ERROR


class AuthenticationFailed(APIException):
    """
    Own AuthenticationFailed created because the one from DRF returns status_code 403
    """
    status_code: int = status.HTTP_401_UNAUTHORIZED
    default_detail: str = ""
    default_code: str = 'authentication_failed'


class KeyRemovedException(PermissionDenied):
    default_detail = constants.API_KEY_REMOVED


class WrongKeyException(AuthenticationFailed):
    default_detail = constants.WRONG_API_KEY


class KeyNotFoundException(AuthenticationFailed):
    default_detail = constants.API_KEY_NOT_FOUND


class WrongParameterException(ParseError):
    default_detail = constants.WRONG_PARAMETER


class ParameterNotSetException(ParseError):
    default_detail = constants.PARAMETERS_NOT_SET


class QueryNotFoundException(NotFound):
    default_detail = constants.QUERY_NOT_FOUND
