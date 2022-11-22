from django.urls import path

from .views import SendNewsletterView

urlpatterns = [
    path("manage-start-send-email-engagement/<pk>", SendNewsletterView.as_view(), name="send_email_engagement"),
]
