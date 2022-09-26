from django.contrib.auth import get_user_model

from apps.api.pagination import StandardResultPagination
from apps.api.views import BaseAPIView
from apps.empresas.api.serializers import (
    BalanceSheetSerializer,
    BasicCompanySerializer,
    CashflowStatementSerializer,
    CompanySerializer,
    ExchangeSerializer,
    IncomeStatementSerializer,
)
from apps.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    Company,
    Exchange,
    IncomeStatement,
)

User = get_user_model()


class AllExchangesAPIView(BaseAPIView):
    serializer_class = ExchangeSerializer
    queryset = Exchange
    pagination_class = StandardResultPagination


class BasicCompanyAPIView(BaseAPIView):
    serializer_class = BasicCompanySerializer
    url_parameters = ["ticker"]


class CompleteCompanyAPIView(BaseAPIView):
    serializer_class = CompanySerializer
    queryset = (Company.objects.fast_full, False)
    url_parameters = ["ticker"]


class CompanyIncomeStatementAPIView(BaseAPIView):
    serializer_class = IncomeStatementSerializer
    limited = True
    url_parameters = ["ticker"]
    queryset = (IncomeStatement.objects.yearly, True)
    fk_lookup_model = "company__ticker"


class CompanyBalanceSheetAPIView(BaseAPIView):
    serializer_class = BalanceSheetSerializer
    limited = True
    queryset = (BalanceSheet.objects.yearly, True)
    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"


class CompanyCashflowStatementAPIView(BaseAPIView):
    serializer_class = CashflowStatementSerializer
    limited = True
    queryset = (CashflowStatement.objects.yearly, True)
    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"
