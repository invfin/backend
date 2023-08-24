from rest_framework.permissions import AllowAny

from src.api.pagination import StandardResultPagination
from src.api.views import BaseAPIView, BasePublicAPIView
from src.escritos.models import Term, TermContent

from .serializers import (
    AllTermsSerializer,
    CompleteTermSerializer,
    SimpleTermSerializer,
    TermContentSerializer,
    TermSerializer,
)


class PublicTermsAPIView(BasePublicAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    lookup_field = "slug"
    many_serializer_class = SimpleTermSerializer
    single_serializer_class = CompleteTermSerializer
    many_queryset = Term.objects.all()
    single_queryset = Term.objects.prefetch_related("term_content_parts", "tags")


class AllTermsAPIView(BaseAPIView):
    """
    Returns all the terms that are clean
    """

    serializer_class = AllTermsSerializer
    queryset = Term.objects.clean_terms, True
    pagination_class = StandardResultPagination
    model_to_track = "ignore"


class TermAPIView(BaseAPIView):
    """
    Returns one term and all his content (TermContents related)
    It can be queryed throught by it's ID or slug
    """

    serializer_class = TermSerializer
    url_parameters = ["slug", "id"]
    model_to_track = Term


class TermContentAPIView(BaseAPIView):
    """
    Not used neither publicly available
    """

    serializer_class = TermContentSerializer
    model = TermContent, True
    model_to_track = Term
