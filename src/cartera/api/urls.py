from django.urls import path

from .views import (
    IncomeAPIView,
    InvestmentAPIView,
    SavingsAPIView,
    SpendingsAPIView,
    NetWorthAPIView,
    TransactionsFromFileAPIView,
)

urlpatterns = [
    path("transactions/", TransactionsFromFileAPIView.as_view(), name="transactions"),
    path("investments/", InvestmentAPIView.as_view(), name="investments"),
    path("investments/<int:id>", InvestmentAPIView.as_view(), name="investments-individual"),
    path("incomes/", IncomeAPIView.as_view(), name="incomes"),
    path("incomes/<int:id>", IncomeAPIView.as_view(), name="incomes-individual"),
    path("net-worth/", NetWorthAPIView.as_view(), name="net-worth"),
    path("net-worth/<int:id>", NetWorthAPIView.as_view(), name="net-worth-individual"),
    path("spendendings/", SpendingsAPIView.as_view(), name="spendings"),
    path("spendings/<int:id>", SpendingsAPIView.as_view(), name="spendings-individual"),
    path("savings/", SavingsAPIView.as_view(), name="savings"),
    path("savings/<int:id>", SavingsAPIView.as_view(), name="savings-individual"),
]
