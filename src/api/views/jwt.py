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

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
