from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.api.pagination import StandardResultPagination
from src.notifications.models import Notification

from .serializers import (
    NotificationSerializer,
)


class PublicNotificationsAPIView(ListAPIView):
    # TODO: improve
    queryset = Notification.objects.filter(is_seen=False)
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
