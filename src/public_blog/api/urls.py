from django.urls import path

from .views import (
    PublicBlogsAPIView,
)

urlpatterns = [
    path("blogs/", PublicBlogsAPIView.as_view(), name="blogs-api"),
]
