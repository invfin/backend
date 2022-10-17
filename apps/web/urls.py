from django.urls import path

from .views import (
    ExcelRedirectView,
    HomePage,
    LegalPages,
    soporte_view,
    ManageWebView,
    ManageEmailEngagementCreateView,
    ManageEmailEngagementUpdateView,
    ManageEmailEngagementListView,
    ManageTermListView,
    ManageTermUpdateView,
    send_email_management,
    AutomaticEmailNewsletterView,
)

app_name = "web"
urlpatterns = [
    path("", HomePage.as_view(), name="inicio"),
    path("asuntos-legales/<slug>", LegalPages.as_view(), name="asuntos_legales"),
    path("excel-analisis/", ExcelRedirectView.as_view(), name="excel"),
    path("soporte/", soporte_view, name="soporte"),
    path("manage-web/", ManageWebView.as_view(), name="manage_web"),
    path("manage-list-emails-engament/", ManageEmailEngagementListView.as_view(), name="list_emails_engagement"),
    path("manage-create-email-engament/", ManageEmailEngagementCreateView.as_view(), name="create_email_engagement"),
    path(
        "manage-update-email-engament/<pk>", ManageEmailEngagementUpdateView.as_view(), name="update_email_engagement"
    ),
    path("manage-start-send-email-engagement/<pk>", send_email_management, name="send_email_engagement"),
    path("manage-terms/", ManageTermListView.as_view(), name="manage_all_terms"),
    path("manage-term/<slug>/", ManageTermUpdateView.as_view(), name="manage_single_term"),
    path("automatic-newsletter-creation", AutomaticEmailNewsletterView.as_view(), name="automatic_creation_newsletter"),
]
