from apps.api.pagination import StandardResultPagination
from apps.api.views import BaseAPIView
from apps.escritos.models import Term, TermContent

from .serializers import AllTermsSerializer, TermContentSerializer, TermSerializer


class AllTermsAPIView(BaseAPIView):
    """
    Returns all the terms that are clean
    """

    serializer_class = AllTermsSerializer
    queryset = (Term.objects.clean_terms, True)
    pagination_class = StandardResultPagination


class TermAPIView(BaseAPIView):
    """
    Returns one term and all his content (TermContents related)
    It can be queryed throught by it's ID or slug
    """

    serializer_class = TermSerializer
    url_parameters = ["slug", "id"]


class TermContentAPIView(BaseAPIView):
    """
    Not used neither publicly available
    """

    serializer_class = TermContentSerializer
    queryset = TermContent
