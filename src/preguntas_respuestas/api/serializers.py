from rest_framework.serializers import ModelSerializer

from src.empresas.models import ExchangeOrganisation


class ExchangeOrganisationSerializer(ModelSerializer):
    class Meta:
        model = ExchangeOrganisation
        exclude = ["id"]
