import json

from typing import List

from django.db.models import Q
from django.http.response import HttpResponse

from .api.serializers import (
    ExcelBalanceSheetSerializer,
    ExcelCashflowStatementSerializer,
    ExcelIncomeStatementSerializer,
)
from .api.views import BaseAPIView
from .models import BalanceSheet, CashflowStatement, Company, IncomeStatement


class Suggestor:
    @classmethod
    def suggest_companies(cls, query: str) -> List[str]:
        companies_availables = Company.objects.filter(
            Q(name__icontains=query) | Q(ticker__icontains=query),
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        )[:10]
        return [f"{company.name} [{company.ticker}]" for company in companies_availables]

    @classmethod
    def companies_searcher(cls, request) -> HttpResponse:
        query = request.GET.get("term", "")
        results = Suggestor.suggest_companies(query)
        return HttpResponse(json.dumps(results), "application/json")


def companies_searcher(request) -> HttpResponse:
    return Suggestor.companies_searcher(request)


class BaseExcelAPIView(BaseAPIView):
    """
    Used to share across API endpoints that serve the Inteligent Excel
    It will lookup for "ticker" in the url parameters and will look for the company's ticker
    """

    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"
    limited = True
    is_excel = True
    model_to_track = "Company"


class ExcelAPIIncome(BaseExcelAPIView):
    """
    Used to serves the Inteligent Excel with the company's income statements
    """

    # queryset = (IncomeStatement.objects.yearly, True)
    queryset = (IncomeStatement.objects.yearly, True)
    serializer_class = ExcelIncomeStatementSerializer


class ExcelAPIBalance(BaseExcelAPIView):
    """
    Used to serves the Inteligent Excel with the company's balance sheets
    """

    # queryset = (BalanceSheet.objects.yearly, True)
    queryset = (BalanceSheet.objects.yearly, True)
    serializer_class = ExcelBalanceSheetSerializer


class ExcelAPICashflow(BaseExcelAPIView):
    """
    Used to serves the Inteligent Excel with the company's cashflow statements
    """

    # queryset = (CashflowStatement.objects.yearly, True)
    queryset = (CashflowStatement.objects.yearly, True)
    serializer_class = ExcelCashflowStatementSerializer
