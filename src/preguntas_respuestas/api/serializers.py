from rest_framework.serializers import ModelSerializer, StringRelatedField

from src.preguntas_respuestas.models import (
    Answer,
    AnswerComment,
    QuesitonComment,
    Question,
)
from src.users.api.serializers import AuthorSerializer


class ManyQuestionSerializer(ModelSerializer):
    author = AuthorSerializer()
    category = StringRelatedField()
    tags = StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = [
            "title",
            "slug",
            "category",
            "tags",
            "checkings",
            "total_votes",
            "total_views",
            "is_answered",
            "has_accepted_answer",
            "total_upvotes",
            "total_downvotes",
        ]


class QuestionSerializer(ModelSerializer):
    author = AuthorSerializer()
    category = StringRelatedField()
    tags = StringRelatedField(many=True)

    class Meta:
        model = Question
        exclude = []


class AnswerSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Answer
        fields = [
            "author",
            "content",
            "is_accepted",
            "total_votes",
        ]


class QuesitonCommentSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = QuesitonComment
        exclude = []


class AnswerCommentSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = AnswerComment
        exclude = []
