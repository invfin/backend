from django.urls import path

from .views import (
    AllTermsAPIView,
    PublicTermsAPIView,
    TermAPIView,
)

urlpatterns = [
    path("lista-terminos/", AllTermsAPIView.as_view(), name="all_terms_api"),
    path("termino/", TermAPIView.as_view(), name="term_api"),
    path("terms/", PublicTermsAPIView.as_view(), name="terms-api"),
    path("terms/<str:slug>/", PublicTermsAPIView.as_view(), name="list-terms-api"),
]
