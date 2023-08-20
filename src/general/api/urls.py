from django.urls import path

from .views import PublicSearchAPIView

urlpatterns = [
    path("search/", PublicSearchAPIView.as_view(), name="public-search-api"),
]
