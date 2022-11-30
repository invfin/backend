from typing import Any, Dict
from rest_framework import parsers, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from django.apps import apps
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from apps.notifications.tasks import prepare_notification_task
from apps.notifications import constants


class BaseVoteAndCommentView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    success_message: str = ""
    notification_type: str = ""
    object: type = None  # type: ignore
    url_info: Dict[str, Any] = {}

    def get_object(self, app_label: str, object_name: str, id: int) -> type:
        modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
        self.object = modelo
        return self.object

    def success_url(self):
        return redirect(self.object.get_absolute_url())

    def parse_url(self, url_encoded):
        decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
        for index, info in enumerate(self.url_info):
            self.url_info[info] = decoded_url[index]
        return self.url_info

    def action(self, *args, **kwargs):
        raise NotImplementedError

    def put(self, request, url_encoded, *args, **kwargs):
        pass

    def post(self, request, url_encoded, *args, **kwargs):
        pass


class CreateCommentView(BaseVoteAndCommentView):
    success_message: str = "Comentario agregado"
    notification_type: str = constants.NEW_COMMENT
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": ""}


@login_required
def create_comment_view(request, url_encoded):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            content = request.POST.get("comment_content")
            decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
            id, app_label, object_name = decoded_url[0], decoded_url[1], decoded_url[2]
            modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
            comment = modelo.comments_related.create(author=user, content=content, content_related=modelo)
            prepare_notification_task.delay(comment.dict_for_task, constants.NEW_COMMENT)
            messages.success(request, "Comentario agregado")
        return redirect(modelo.get_absolute_url())


@login_required
def create_vote_view(request, url_encoded):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
            id, app_label, object_name, vote = decoded_url[0], decoded_url[1], decoded_url[2], decoded_url[3]
            modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
            if modelo.author == user:
                messages.error(request, "No puedes votarte a ti mismo")
                return redirect(modelo.get_absolute_url())
            vote_result = modelo.vote(user, vote)
            if vote_result == 0:
                messages.error(request, "Ya has votado")
                return redirect(modelo.get_absolute_url())
            prepare_notification_task.delay(modelo.dict_for_task, constants.NEW_VOTE)
            messages.success(request, "Voto aportado")
        return redirect(modelo.get_absolute_url())
