from django.urls import path

from .views import (
    GlosarioView,
    TermCorrectionView,
    TermDetailsView,
    ManageUserTermCorrectionListView,
    ManageUserTermCorrectionDetailView,
)

app_name = "escritos"
urlpatterns = [
    path("diccionario-financiero/", GlosarioView.as_view(), name="glosario"),
    path("definicion/<slug>/", TermDetailsView.as_view(), name="single_term"),
    path("correction/<pk>", TermCorrectionView.as_view(), name="correction_term"),
    path("users-corrections-to-review/", ManageUserTermCorrectionListView.as_view(), name="manage_all_corrections"),
    path("correction-to-review/<pk>/", ManageUserTermCorrectionDetailView.as_view(), name="manage_user_correction"),
]
