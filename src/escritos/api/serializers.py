from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    StringRelatedField,
    URLField,
)

from src.api.serializers import RichTextField
from src.escritos.api.abstract import AbstractWrittenContentSerializer
from src.escritos.models import Term, TermContent


class TermContentSerializer(ModelSerializer):
    titulo = CharField(source="title")
    orden = CharField(source="order")
    contenido = RichTextField(source="content")
    link = URLField()

    class Meta:
        model = TermContent
        fields = ["id", "titulo", "orden", "contenido", "link"]


class TermSerializer(ModelSerializer):
    partes = TermContentSerializer(source="term_content_parts", many=True)
    titulo = CharField(source="title")
    resumen = CharField(source="resume")
    votos_totales = IntegerField(source="total_votes")
    visitas_totales = IntegerField(source="total_views")
    veces_compartido = IntegerField(source="times_shared")
    categoria = StringRelatedField(source="category")
    autor = StringRelatedField(source="author")
    imagen = CharField(source="image")
    link = URLField()

    class Meta:
        model = Term
        fields = [
            "id",
            "titulo",
            "slug",
            "link",
            "resumen",
            "votos_totales",
            "visitas_totales",
            "veces_compartido",
            "categoria",
            "autor",
            "imagen",
            "partes",
        ]


class AllTermsSerializer(TermSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("partes")


class SimpleTermSerializer(AbstractWrittenContentSerializer):
    class Meta(AbstractWrittenContentSerializer.Meta):
        model = Term


class CompleteTermContentSerializer(ModelSerializer):
    # content = RichTextField()
    link = URLField()

    class Meta:
        model = TermContent
        fields = ["id", "title", "order", "content", "link"]


class CompleteTermSerializer(ModelSerializer):
    term_parts = CompleteTermContentSerializer(many=True)
    link = URLField()
    category = StringRelatedField()
    tags = StringRelatedField(many=True)

    class Meta:
        model = Term
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "link",
            "resume",
            "published_at",
            "current_status",
            "image",
            "tags",
            "term_parts",
        ]
