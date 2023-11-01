from itertools import chain
from typing import Any, Dict, List

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Case, CharField, F, Value, When
from django.db.models.functions import Concat
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from src.api.pagination import StandardResultPagination
from src.empresas.models import Company
from src.escritos.constants import BASE_ESCRITO_PUBLISHED
from src.escritos.models import Term, TermContent
from src.notifications import constants

from .mixins import BaseVoteAndCommentMixin


class PublicSearchAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultPagination
    annotated_values = ["pk", "title", "path", "logo", "rank", "inside"]
    order_by = "-rank"
    sliced_by = 10

    def get(self, *args, **kwargs):
        return JsonResponse(self.search(), safe=False)

    def search(self) -> List[Dict[str, Any]]:
        search = self.request.query_params.get("search", "")
        filters = self.request.query_params.get("filter", "all")
        results = self.find_results(search, filters)
        return sorted(results, key=lambda x: x["rank"], reverse=True)[: self.sliced_by]

    def find_results(self, search: str, filters: str) -> List[Dict[str, Any]]:
        query = SearchQuery(search)
        finders = {
            "company": [self.find_companies],
            "all": [self.find_companies, self.find_content_terms, self.find_terms],
        }
        return list(chain.from_iterable([x(query) for x in finders[filters]]))

    def find_companies(self, query: SearchQuery) -> List[Dict[str, str | float | int]]:
        return list(
            Company.objects.search(query)
            .values(*self.annotated_values)
            .order_by(self.order_by)[: self.sliced_by]
        )

    def find_content_terms(self, query: SearchQuery) -> List[Dict[str, Any]]:
        return list(
            TermContent.objects.filter(term_related__status=BASE_ESCRITO_PUBLISHED)
            .annotate(
                inside=Value("diccionario"),
                logo=Case(
                    When(
                        term_related__thumbnail__isnull=False,
                        then="term_related__thumbnail",
                    ),
                    When(
                        term_related__non_thumbnail_url__isnull=False,
                        then="term_related__non_thumbnail_url",
                    ),
                    default=Value("/static/general/assets/img/general/why-us.webp"),
                    output_field=CharField(),
                ),
                rank=SearchRank(SearchVector("title"), query),
                path=Concat(
                    "term_related__slug",
                    Value("#"),
                    "title",
                ),
            )
            .values(*self.annotated_values)
            .order_by(self.order_by)[: self.sliced_by]
        )

    def find_terms(self, query: SearchQuery) -> List[Dict[str, Any]]:
        return list(
            Term.objects.filter(status=BASE_ESCRITO_PUBLISHED)
            .annotate(
                inside=Value("diccionario"),
                logo=Case(
                    When(thumbnail__isnull=False, then="thumbnail"),
                    When(non_thumbnail_url__isnull=False, then="non_thumbnail_url"),
                    default=Value("/static/general/assets/img/general/why-us.webp"),
                    output_field=CharField(),
                ),
                path=F("slug"),
                rank=SearchRank(SearchVector("title"), query),
            )
            .values(*self.annotated_values)
            .order_by(self.order_by)[: self.sliced_by]
        )


class CreateCommentView(BaseVoteAndCommentMixin, APIView):
    success_message: str = "Comentario agregado"
    error_message: str = "Ha habido un error"
    notification_type: str = constants.NEW_COMMENT
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": ""}

    def create_comment(self):
        content = self.request.POST.get("comment_content")
        return self.object.comments_related.create(
            author=self.request.user,
            content=content,
        )

    def action(self, url_encoded) -> type:
        self.get_object(url_encoded)
        return self.create_comment()


class VoteView(BaseVoteAndCommentMixin, APIView):
    success_message: str = "Voto agregado"
    error_message: str = "Ha habido un error"
    notification_type: str = constants.NEW_VOTE
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": "", "vote": ""}

    def manage_vote(self, modelo: type):
        user = self.request.user
        vote = self.url_info["vote"]
        # TODO the author == user condidition should be inside the vote method
        if modelo.author == user:
            self.error_message = "No puedes votarte a ti mismo"
            raise Exception
        vote_result = modelo.vote(user, vote)
        if vote_result == 0:
            self.error_message = "Ya has votado"
            raise Exception
        return modelo

    def action(self, url_encoded) -> type:
        obj = self.get_object(url_encoded)
        return self.manage_vote(obj)
