from django.urls import path

from .views import (
    ExcelRedirectView, 
    HomePage, 
    LegalPages, 
    soporte_view,
    CreateWebEmailView,
    WebEngagementView,
)

app_name = "web"
urlpatterns = [

    path('', HomePage.as_view(), name="inicio"),
    
    path('asuntos-legales/<slug>', LegalPages.as_view(), name="asuntos_legales"),

    path('excel-analisis/', ExcelRedirectView.as_view(), name="excel"),
    path('soporte/', soporte_view, name="soporte"),

    path('mensaje-web/', CreateWebEmailView.as_view(), name="email_web"),
    path('management-engament/', WebEngagementView.as_view(), name="manage_engagement_web"),
]