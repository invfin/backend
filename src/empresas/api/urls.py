from django.urls import path

from .views import (
    AllExchangesAPIView,
    BasicCompanyAPIView,
    CompanyBalanceSheetAPIView,
    CompanyCashflowStatementAPIView,
    CompanyIncomeStatementAPIView,
    CompleteCompanyAPIView,
    PublicCompanyAPIView,
)

urlpatterns = [
    path("companies/", PublicCompanyAPIView.as_view(), name="company-list"),
    # Currently using
    path("lista-exchanges/", AllExchangesAPIView.as_view()),
    path("empresa-completa/", CompleteCompanyAPIView.as_view()),
    path("empresa-basica/", BasicCompanyAPIView.as_view()),
    path("estado-resultados/", CompanyIncomeStatementAPIView.as_view()),
    path("balance-general/", CompanyBalanceSheetAPIView.as_view()),
    path("estado-flujo-efectivo/", CompanyCashflowStatementAPIView.as_view()),
]
