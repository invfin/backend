from django.urls import path

from .views import UserJWTView

urlpatterns = [
    # Your other URL patterns
    path("users/", UserJWTView.as_view(), name="users-jwt"),
]
