from src.api.pagination import StandardResultPagination
from src.api.views import BaseAPIView
from src.industries_sectors.api.serializers import IndustrySerializer, SectorSerializer
from src.industries_sectors.models import Industry, Sector


class AllIndustriesAPIView(BaseAPIView):
    serializer_class = IndustrySerializer
    queryset = (Industry.objects.all, True)
    pagination_class = StandardResultPagination
    model_to_track = "ignore"


class AllSectorsAPIView(BaseAPIView):
    serializer_class = SectorSerializer
    queryset = (Sector.objects.all, True)
    pagination_class = StandardResultPagination
    model_to_track = "ignore"
