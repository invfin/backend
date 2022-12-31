from .web_management import (
    AutomaticEmailNewsletterView,
    ManageEmailEngagementCreateView,
    ManageEmailEngagementListView,
    ManageEmailEngagementUpdateView,
    ManagePreviewEmailEngagementDetailsView,
    ManageTermListView,
    ManageTermUpdateView,
    ManageWebView,
)
from .web_regular import ExcelRedirectView, HomePage, LegalPages, RoadmapDetailView, RoadmapListView, SupportFormView

__all__ = [
    "AutomaticEmailNewsletterView",
    "ManageWebView",
    "ManageTermListView",
    "ManageTermUpdateView",
    "ManageEmailEngagementCreateView",
    "ManageEmailEngagementListView",
    "ManageEmailEngagementUpdateView",
    "ManagePreviewEmailEngagementDetailsView",
    "HomePage",
    "RoadmapListView",
    "RoadmapDetailView",
    "LegalPages",
    "SupportFormView",
    "ExcelRedirectView",
]
