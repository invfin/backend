from typing import Any, Dict

from django.apps import apps
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from src.notifications.tasks import prepare_notification_task


class ParseEncodedUrlMixin:
    object: type = None  # type: ignore
    url_info: Dict[str, Any] = {}

    def get_url_info(self):
        if not self.url_info:
            raise NotImplementedError("url_info is required")

    def build_object(self, app_label: str, object_name: str, id: int, **kwargs) -> type:
        return apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)

    def parse_url(self, url_encoded: str) -> Dict[str, Any]:
        decoded_url = force_str(urlsafe_base64_decode(url_encoded)).split("-")
        for index, info in enumerate(self.url_info):
            self.url_info[info] = decoded_url[index]
        return self.url_info

    def get_object(self, url_encoded: str) -> type:
        url_info = self.parse_url(url_encoded)
        self.object = self.build_object(**url_info)
        return self.object


class BaseVoteAndCommentMixin(ParseEncodedUrlMixin):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["post"]
    success_message: str = ""
    notification_type: str = ""
    error_message: str = ""

    def success_url(self) -> str:
        return self.object.get_absolute_url()

    def send_notification_and_message(self, model: type) -> None:
        prepare_notification_task.delay(model.dict_for_task, self.notification_type)
        messages.success(self.request, self.success_message)

    def action(*args, **kwargs):
        raise NotImplementedError

    def response(self, encoded_url):
        try:
            obj = self.action(encoded_url)
        except Exception:
            messages.error(self.request, self.error_message)
        else:
            self.send_notification_and_message(obj)
        finally:
            return redirect(self.success_url())

    def post(self, *args, **kwargs):
        url_encoded = self.kwargs["url_encoded"]
        return self.response(url_encoded)
