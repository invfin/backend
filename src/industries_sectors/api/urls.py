from django.urls import path

from .views import AllIndustriesAPIView, AllSectorsAPIView

urlpatterns = [
    path("lista-industrias/", AllIndustriesAPIView.as_view()),
    path("lista-sectores/", AllSectorsAPIView.as_view()),
]
