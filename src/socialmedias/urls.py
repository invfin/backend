from django.urls import path

from .views import FacebookAuthRedirectView, ManageAddSocialmediasTempalteView, ManageSocialmediasView

app_name = "socialmedias"
urlpatterns = [
    path("facebook-auth/", FacebookAuthRedirectView.as_view(), name="facebook-auth-redirect-url"),
    path("manage-socialmedias/", ManageSocialmediasView.as_view(), name="manage-socialmedias"),
    path("add-new-auth-socialmedias/", ManageAddSocialmediasTempalteView.as_view(), name="add-new-auth-socialmedias"),
]
