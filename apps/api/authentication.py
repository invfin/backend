from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .constants import WRONG_API_KEY, API_KEY_REMOVED, NO_API_KEY
from .models import Key


class KeyAuthentication(BaseAuthentication):
    # TODO Should we do only one query to check if the key exists and is active?
    def authenticate(self, request):
        key = request.GET.get("api_key")
        if key:
            if Key.objects.filter(key=key).exists():
                if Key.objects.key_is_active(key):
                    key = Key.objects.get_key(key)
                    return (key.user, key)
                raise AuthenticationFailed(API_KEY_REMOVED)
            raise AuthenticationFailed(WRONG_API_KEY)
        raise AuthenticationFailed(NO_API_KEY)
