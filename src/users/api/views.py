from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin

from src.api.authentication import JWTAuthentication
from src.api.permissions import ReadOnly
from src.users.models import User

from .serializers import CreateUserSerializer, GetUserSerializer, UpdateUserSerializer


class UserJWTView(RetrieveUpdateAPIView, CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [ReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_classes = {
        "POST": CreateUserSerializer,
        "PUT": UpdateUserSerializer,
        "GET": GetUserSerializer,
        "PATCH": UpdateUserSerializer,
    }

    def get_serializer_class(self):
        if action := self.request.method:
            return self.serializer_classes[action]
        raise MethodNotAllowed(f"{action}")

    def get_object(self) -> User:
        return self.request.user  # type: ignore
