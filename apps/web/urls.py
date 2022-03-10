from django.urls import path
from .views import (
    HomePage,
    LegalPages,
    ExcelView,
    soporte_view
)

app_name = "web"
urlpatterns = [

    path('', HomePage.as_view(), name="inicio"),
    
    path('asuntos-legales/<slug>', LegalPages.as_view(), name="asuntos_legales"),

    path('excel-analisis/', ExcelView.as_view(), name="excel"),
    path('soporte/', soporte_view, name="soporte"),
]