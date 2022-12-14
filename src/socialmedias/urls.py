from django.urls import path

from .views import (
    FacebookAuthRedirectView,
)

app_name = "socialmedias"
urlpatterns = [
    path("facebook-auth/", FacebookAuthRedirectView.as_view(), name="facebook-auth-redirect-url"),
]
