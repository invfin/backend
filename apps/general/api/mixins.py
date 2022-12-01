from typing import Any, Dict

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.apps import apps


class ParseEncodedUrlMixin:
    object: type = None  # type: ignore
    url_info: Dict[str, Any] = {}

    def get_url_info(self):
        if not self.url_info:
            raise NotImplementedError("url_info is required")

    def build_object(self, app_label: str, object_name: str, id: int, **kwargs) -> type:
        return apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)

    def parse_url(self, url_encoded: str) -> Dict[str, Any]:
        decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
        for index, info in enumerate(self.url_info):
            self.url_info[info] = decoded_url[index]
        return self.url_info

    def get_object(self, url_encoded: str) -> type:
        url_info = self.parse_url(url_encoded)
        self.object = self.build_object(**url_info)
        return self.object
