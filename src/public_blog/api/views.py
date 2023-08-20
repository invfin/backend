from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.api.pagination import StandardResultPagination
from src.public_blog.models import PublicBlog

from .serializers import (
    SimpleBlogSerializer,
)


class PublicBlogsAPIView(ListAPIView):
    # TODO: improve
    queryset = PublicBlog.objects.all()
    serializer_class = SimpleBlogSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
