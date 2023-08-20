from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.api.pagination import StandardResultPagination
from src.api.views import BaseAPIView

from ..models import Superinvestor, SuperinvestorActivity, SuperinvestorHistory
from .serializers import (
    SimpleSuperinvestorSerializer,
    SuperinvestorActivitySerializer,
    SuperinvestorHistorySerializer,
    SuperinvestorSerializer,
)

User = get_user_model()


class PublicSuperinvestorsAPIView(ListAPIView):
    # TODO: improve
    queryset = Superinvestor.objects.all()
    serializer_class = SimpleSuperinvestorSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination


class AllSuperinvestorsAPIView(BaseAPIView):
    serializer_class = SuperinvestorSerializer
    queryset = Superinvestor.objects.all, True
    pagination_class = StandardResultPagination
    model_to_track = "ignore"


class SuperinvestorActivityAPIView(BaseAPIView):
    serializer_class = SuperinvestorActivitySerializer
    queryset = SuperinvestorActivity.objects.filter, True
    pagination_class = StandardResultPagination
    url_parameters = ["slug"]
    fk_lookup_model = "superinvestor_related__info_accronym"
    model_to_track = Superinvestor


class SuperinvestorHistoryAPIView(BaseAPIView):
    serializer_class = SuperinvestorHistorySerializer
    queryset = SuperinvestorHistory.objects.filter, True
    pagination_class = StandardResultPagination
    url_parameters = ["slug"]
    fk_lookup_model = "superinvestor_related__info_accronym"
    model_to_track = Superinvestor
