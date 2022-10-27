from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.api.constants import WRONG_API_KEY, API_KEY_REMOVED, NO_API_KEY
from apps.api.models import Key


class KeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.GET.get("api_key")
        if key:
            try:
                key_obj = Key.objects.get(key=key)
            except Key.DoesNotExist:
                raise AuthenticationFailed(WRONG_API_KEY)
            else:
                if key_obj.in_use:
                    # DRF wants to receive (request.user, request.auth)
                    # https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
                    return (key_obj.user, key_obj)
                else:
                    raise AuthenticationFailed(API_KEY_REMOVED)
        raise AuthenticationFailed(NO_API_KEY)
