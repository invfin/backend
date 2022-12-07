import base64
from typing import Any, Dict

from django.http.response import HttpResponse
from django.utils import timezone

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from src.api.permissions import ReadOnly
from src.general.api.mixins import ParseEncodedUrlMixin

from .constants import PIXEL_GIF_BYTES


class EmailOpeningView(ParseEncodedUrlMixin, APIView):
    authentication_classes = []
    permission_classes = [ReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": ""}

    def save_email_opened(self, model):
        model.opened = True
        model.date_opened = timezone.now()
        model.save(update_fields=["opened", "date_opened"])

    def action(self, uidb64) -> bytes:
        model = self.get_object(uidb64)
        self.save_email_opened(model)
        return base64.b64decode(PIXEL_GIF_BYTES)

    def get(self, request, uidb64, *args, **kwargs):
        pixel_gif = self.action(uidb64)
        return HttpResponse(pixel_gif, content_type="image/gif")
