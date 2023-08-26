from src.api.views import BasePublicAPIView
from src.preguntas_respuestas.api.serializers import (
    ManyQuestionSerializer,
    QuestionSerializer,
)
from src.preguntas_respuestas.models import (
    Question,
)


class PublicQuestionAPIView(BasePublicAPIView):
    # TODO: finish that
    many_serializer_class = ManyQuestionSerializer
    single_serializer_class = QuestionSerializer
    many_queryset = Question.objects.many_api_query()
    single_queryset = Question.objects.single_api_query()
    lookup_field = "slug"
