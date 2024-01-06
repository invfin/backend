from django.conf import settings
from django.urls import include, path

from src.api.views import (
    APIDocumentation,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    request_API_key,
)

API_version = settings.API_VERSION["CURRENT_VERSION"]

app_name = "api"
urlpatterns = [
    path(f"{API_version}/", include("src.general.api.urls")),
    path(f"{API_version}/", include("src.screener.api.urls")),
    path(f"{API_version}/", include("src.public_blog.api.urls")),
    path(f"{API_version}/", include("src.notifications.api.urls")),
    path(f"{API_version}/", include("src.escritos.api.urls")),
    path(f"{API_version}/", include("src.empresas.api.urls")),
    path(f"{API_version}/", include("src.super_investors.api.urls")),
    path(f"{API_version}/", include("src.industries_sectors.api.urls")),
    path(f"{API_version}/", include("src.users.api.urls")),
    path(f"{API_version}/", include("src.cartera.api.urls")),
    path("request-api-key/", request_API_key, name="request_api_key"),
    path("api-documentacion/", APIDocumentation.as_view(), name="api_documentation"),
    path(f"{API_version}/jwt-token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(f"{API_version}/jwt-token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        f"{API_version}/jwt-token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
