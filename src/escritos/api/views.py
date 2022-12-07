from src.api.pagination import StandardResultPagination
from src.api.views import BaseAPIView
from src.escritos.models import Term, TermContent

from .serializers import AllTermsSerializer, TermContentSerializer, TermSerializer


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
