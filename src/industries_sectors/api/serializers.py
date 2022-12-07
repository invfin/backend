from rest_framework.serializers import CharField, ModelSerializer

from src.industries_sectors.models import Industry, Sector


class IndustrySerializer(ModelSerializer):
    industria = CharField(source="industry")

    class Meta:
        model = Industry
        fields = ["id", "industria"]


class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = ["id", "sector"]
