from typing import Optional

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.api.pagination import StandardResultPagination
from src.api.views import BasePublicAPIView

from ..models import (
    CashflowMovementCategory,
    Income,
    Investment,
    Saving,
    Spend,
)
from .serializers import (
    CashflowMovementCategorySerializer,
    IncomeSerializer,
    InvestmentSerializer,
    SavingSerializer,
    SpendSerializer,
    TransactionsFromFileSerializer,
)


class TransactionsFromFileAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = TransactionsFromFileSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"details": "success"}, status=status.HTTP_201_CREATED)


class CashflowMovementCategoryAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = CashflowMovementCategorySerializer
    lookup_field = "id"
    serializer_class = SavingSerializer
    many_queryset = CashflowMovementCategory.objects.prefetch_related("user").all()
    single_queryset = CashflowMovementCategory.objects.prefetch_related("user").all()


class InvestmentAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = InvestmentSerializer
    many_queryset = Investment.objects.select_related("user").all()
    single_queryset = Investment.objects.select_related("user").all()

    def get(self, *args, **kwargs):
        if kwargs.get(self.lookup_field):
            return self.single(*args, **kwargs)
        return self.many(*args, **kwargs)

    def get_movements(self) -> Optional[int]:
        pass


class IncomeAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = IncomeSerializer
    many_queryset = Income.objects.prefetch_related("user")
    single_queryset = Income.objects.prefetch_related("user")


class SpendAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = SpendSerializer
    many_queryset = Spend.objects.prefetch_related("user")
    single_queryset = Spend.objects.prefetch_related("user")


class SavingAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = SavingSerializer
    many_queryset = Saving.objects.prefetch_related("user")
    single_queryset = Saving.objects.prefetch_related("user")
