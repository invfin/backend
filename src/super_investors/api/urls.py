from django.urls import path

from .views import (
    AllSuperinvestorsAPIView,
    PublicSuperinvestorsAPIView,
    SuperinvestorActivityAPIView,
    SuperinvestorHistoryAPIView,
)

urlpatterns = [
    path(
        "superinvestors/",
        PublicSuperinvestorsAPIView.as_view(),
        name="superinvestors-api",
    ),
    path(
        "lista-movimientos/",
        SuperinvestorActivityAPIView.as_view(),
        name="superinvestors_lista_movimientos",
    ),
    path(
        "lista-superinversores/",
        AllSuperinvestorsAPIView.as_view(),
        name="superinvestors_lista_superinversores",
    ),
    path(
        "lista-historial/",
        SuperinvestorHistoryAPIView.as_view(),
        name="superinvestors_lista_historial",
    ),
]
