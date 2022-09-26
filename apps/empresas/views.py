import json

from django.db.models import Q
from django.http.response import HttpResponse

from .api.serializers import (
    ExcelBalanceSheetSerializer,
    ExcelCashflowStatementSerializer,
    ExcelIncomeStatementSerializer,
)
from .api.views import BaseAPIView
from .models import BalanceSheet, CashflowStatement, Company, IncomeStatement


def companies_searcher(request):
    query = request.GET.get("term", "")
    companies_availables = Company.objects.filter(
        Q(name__icontains=query) | Q(ticker__icontains=query),
        no_incs=False,
        no_bs=False,
        no_cfs=False,
    )[:10]

    results = [f"{company.name} [{company.ticker}]" for company in companies_availables]

    data = json.dumps(results)
    return HttpResponse(data, "application/json")


class ExcelAPIIncome(BaseAPIView):
    """
    Used to serves the Inteligent Excel with the company's income statements
    It will lookup for "ticker" in the url parameters and will look for the company's ticker
    """

    queryset = (IncomeStatement.objects.yearly, True)
    serializer_class = ExcelIncomeStatementSerializer
    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"
    limited = True
    is_excel = True
    model_to_track = "Company"


class ExcelAPIBalance(BaseAPIView):
    """
    Used to serves the Inteligent Excel with the company's balance sheets
    It will lookup for "ticker" in the url parameters and will look for the company's ticker
    """

    queryset = (BalanceSheet.objects.yearly, True)
    serializer_class = ExcelBalanceSheetSerializer
    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"
    limited = True


class ExcelAPICashflow(BaseAPIView):
    """
    Used to serves the Inteligent Excel with the company's cashflow statements
    It will lookup for "ticker" in the url parameters and will look for the company's ticker
    """

    queryset = (CashflowStatement.objects.yearly, True)
    serializer_class = ExcelCashflowStatementSerializer
    url_parameters = ["ticker"]
    fk_lookup_model = "company__ticker"
    limited = True
