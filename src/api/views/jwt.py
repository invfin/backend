from datetime import datetime

from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serializers import TokenObtainSerializer


class TokenVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


class TokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def _django_session_key(self, now: datetime) -> str:
        s = SessionStore()
        s["last_login"] = now.timestamp()
        s.create()
        return s.session_key or ""

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        serializer = TokenObtainSerializer(data=request.data, now=now)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["sessionid"] = self._django_session_key(now)
        return Response(data, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
