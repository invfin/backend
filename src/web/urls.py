from django.urls import path

from src.web.api.urls import urlpatterns as api_urlpatterns
from src.web.views import (
    AutomaticEmailNewsletterView,
    ExcelRedirectView,
    HomePage,
    LegalPages,
    ManageEmailEngagementCreateView,
    ManageEmailEngagementListView,
    ManageEmailEngagementUpdateView,
    ManagePreviewEmailEngagementDetailsView,
    ManageTermListView,
    ManageTermUpdateView,
    ManageWebView,
    RoadmapDetailView,
    RoadmapListView,
    soporte_view,
)

app_name = "web"
urlpatterns = [
    path("", HomePage.as_view(), name="inicio"),
    path("asuntos-legales/<slug>/", LegalPages.as_view(), name="asuntos_legales"),
    path("excel-analisis/", ExcelRedirectView.as_view(), name="excel"),
    path("soporte/", soporte_view, name="soporte"),
    path("manage-web/", ManageWebView.as_view(), name="manage_web"),
    path("roadmap/", RoadmapListView.as_view(), name="roadmap"),
    path("roadmap-item/<slug>/", RoadmapDetailView.as_view(), name="roadmap_item"),
    path("manage-list-emails-engament/", ManageEmailEngagementListView.as_view(), name="list_emails_engagement"),
    path("manage-create-email-engament/", ManageEmailEngagementCreateView.as_view(), name="create_email_engagement"),
    path(
        "manage-update-email-engament/<pk>/", ManageEmailEngagementUpdateView.as_view(), name="update_email_engagement"
    ),
    path(
        "manage-preview-email-engament/<pk>/",
        ManagePreviewEmailEngagementDetailsView.as_view(),
        name="preview_email_engagement",
    ),
    path("manage-terms/", ManageTermListView.as_view(), name="manage_all_terms"),
    path("manage-term/<slug>/", ManageTermUpdateView.as_view(), name="manage_single_term"),
    path(
        "automatic-newsletter-creation/", AutomaticEmailNewsletterView.as_view(), name="automatic_creation_newsletter"
    ),
] + api_urlpatterns
