from django.urls import path

from .views import (
    IncomeAPIView,
    InvestmentAPIView,
    SavingAPIView,
    SpendAPIView,
)

urlpatterns = [
    path("investments/", InvestmentAPIView.as_view(), name="investments"),
    path("investments/<int:id>", InvestmentAPIView.as_view(), name="investments-individual"),
    path("incomes/", IncomeAPIView.as_view(), name="incomes"),
    path("incomes/<int:id>", IncomeAPIView.as_view(), name="incomes-individual"),
    path("spends/", SpendAPIView.as_view(), name="spends"),
    path("spends/<int:id>", SpendAPIView.as_view(), name="spends-individual"),
    path("savings/", SavingAPIView.as_view(), name="savings"),
    path("savings/<int:id>", SavingAPIView.as_view(), name="savings-individual"),
]
