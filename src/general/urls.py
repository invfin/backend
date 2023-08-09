from django.urls import path

from .api.views import CreateCommentView, VoteView
from .views import (
    ComingSoonview,
    MessagesTemplateview,
    NotificationsListView,
    delete_notification,
    search_results,
    suggest_list_search,
    update_favorites,
)

app_name = "general"
urlpatterns = [
    path(
        "create-comment/<url_encoded>/",
        CreateCommentView.as_view(),
        name="create_comment_view",
    ),
    path("create-vote/<url_encoded>/", VoteView.as_view(), name="create_vote_view"),
    path("suggestions-buscador/", suggest_list_search, name="searcher_suggestions"),
    path("buscador/", search_results, name="searcher"),
    path("update-favs/", update_favorites, name="update_favorites"),
    path("coming-soon/", ComingSoonview.as_view(), name="coming_soon"),
    path("tus-notificaciones/", NotificationsListView.as_view(), name="notifications_list"),
    path("delete-notif/<notif_id>/", delete_notification, name="notification_delete"),
    path("return-nav-messages/", MessagesTemplateview.as_view(), name="nav_messages"),
]
