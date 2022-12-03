from django.urls import path

from .views import AllSuperinvestorsAPIView, SuperinvestorActivityAPIView, SuperinvestorHistoryAPIView

urlpatterns = [
    path("lista-movimientos/", SuperinvestorActivityAPIView.as_view(), name="superinvestors_lista_movimientos"),
    path("lista-superinversores/", AllSuperinvestorsAPIView.as_view(), name="superinvestors_lista_superinversores"),
    path("lista-historial/", SuperinvestorHistoryAPIView.as_view(), name="superinvestors_lista_historial"),
]
