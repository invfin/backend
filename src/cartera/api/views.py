from decimal import Decimal
from typing import Optional
from django.db.models.query import QuerySet, F
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from src.periods.models import Period
from src.api.pagination import StandardResultPagination
from src.api.views import BasePublicAPIView
from django.db.models.functions.comparison import NullIf
from ..models import (
    CashflowMovementCategory,
    Income,
    Investment,
    Savings,
    Spendings,
    NetWorth,
)
from .serializers import (
    CashflowMovementCategorySerializer,
    NetWorthSerializer,
    IncomeSerializer,
    InvestmentSerializer,
    SavingsSerializer,
    SpendingsSerializer,
    TransactionsFromFileSerializer,
)
from src.users.models import User


class PortfolioInitailAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()  # TODO: add jwt auth
    lookup_field = ""

    def get_queryset(self) -> QuerySet:
        num_periods = self.request.query_params.get("periods", 8)
        periods = Period.objects.all()[:num_periods].values_list("id", flat=True)
        # TODO: remove the user and get it from the request
        user = User.objects.get(id=1)
        return NetWorth.objects.filter(user=user, period_id__in=periods)


class TransactionsFromFileAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = TransactionsFromFileSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "success"}, status=status.HTTP_201_CREATED)


class CashflowMovementCategoryAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = CashflowMovementCategorySerializer
    lookup_field = "id"
    serializer_class = SavingsSerializer
    many_queryset = CashflowMovementCategory.objects.prefetch_related("user").all()
    single_queryset = CashflowMovementCategory.objects.prefetch_related("user").all()


class NetWorthAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = NetWorthSerializer
    many_queryset = (
        NetWorth.objects.prefetch_related("user")
        .order_by(
            "period__year",
            "period__period",
        )
        .values(
            "period__year",
            "period__period",
        )
        .annotate(
            percent_savings=F("savings") / NullIf(F("equity"), Decimal("0.0")),
            percent_investments=F("investments") / NullIf(F("equity"), Decimal("0.0")),
            percent_spendings=F("spendings") / NullIf(F("equity"), Decimal("0.0")),
        )
        .values(
            "period__year",
            "period__period",
            "equity",
            "percent_savings",
            "percent_investments",
            "percent_spendings",
            "savings",
            "spendings",
            "incomes",
            "investments",
        )
    )
    single_queryset = NetWorth.objects.prefetch_related("user")


class InvestmentAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = InvestmentSerializer
    many_queryset = Investment.objects.select_related("user").all()
    single_queryset = Investment.objects.select_related("user").all()

    def get_movements(self) -> Optional[int]:
        pass


class IncomeAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = IncomeSerializer
    many_queryset = Income.objects.prefetch_related("user")
    single_queryset = Income.objects.prefetch_related("user")


class SpendingsAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = SpendingsSerializer
    many_queryset = Spendings.objects.prefetch_related("user")
    single_queryset = Spendings.objects.prefetch_related("user")


class SavingsAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "id"
    serializer_class = SavingsSerializer
    many_queryset = Savings.objects.prefetch_related("user")
    single_queryset = Savings.objects.prefetch_related("user")
