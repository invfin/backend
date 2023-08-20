from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
)

from src.users.api.serializers import AuthorSerializer


class AbstractWrittenContentSerializer(ModelSerializer):
    views = IntegerField(source="total_views")
    author = AuthorSerializer()

    class Meta:
        fields = [
            "title",
            "slug",
            "resume",
            "image",
            "views",
            "author",
        ]
