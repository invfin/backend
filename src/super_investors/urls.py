from django.urls import path

from .views import (
    AllSuperinvestorsView,
    SuperinvestorView,
    return_portfolios_with_company,
    return_superinvestor_movements,
)

app_name = "super_investors"
urlpatterns = [
    path(
        "las-mejores-carteras-del-mundo/",
        AllSuperinvestorsView.as_view(),
        name="all_superinvestors",
    ),
    path("cartera-de/<slug>/", SuperinvestorView.as_view(), name="superinvestor"),
    path(
        "superinvestor-movements-late-response/<id>/",
        return_superinvestor_movements,
        name="return_superinvestor_movements",
    ),
    path(
        "portfolios-with-company/<company_id>/",
        return_portfolios_with_company,
        name="return_portfolios_with_company",
    ),
]
