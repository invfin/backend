from django.urls import path

from .views import EmailOpeningView

app_name = "emailing"
urlpatterns = [
    path("email-image/<uidb64>/", EmailOpeningView.as_view(), name="email_opened_view"),
]
