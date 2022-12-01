from typing import Any, Dict
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib import messages
from django.shortcuts import redirect

from apps.notifications.tasks import prepare_notification_task
from apps.notifications import constants

from .mixins import ParseEncodedUrlMixin


class BaseVoteAndCommentView(ParseEncodedUrlMixin, APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
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

    def response(self, url_encoded):
        try:
            obj = self.action(url_encoded)
        except Exception:
            messages.error(self.request, self.error_message)
        else:
            self.send_notification_and_message(obj)
        finally:
            return redirect(self.success_url())

    def post(self, request, url_encoded, *args, **kwargs):
        return self.response(url_encoded)


class CreateCommentView(BaseVoteAndCommentView):
    success_message: str = "Comentario agregado"
    error_message: str = "Ha habido un error"
    notification_type: str = constants.NEW_COMMENT
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": ""}

    def create_comment(self):
        content = self.request.POST.get("comment_content")
        return self.object.comments_related.create(
            author=self.request.user,
            content=content,
        )

    def action(self, url_encoded) -> type:
        self.get_object(url_encoded)
        return self.create_comment()


class VoteView(BaseVoteAndCommentView):
    success_message: str = "Voto agregado"
    error_message: str = "Ha habido un error"
    notification_type: str = constants.NEW_VOTE
    url_info: Dict[str, Any] = {"id": "", "app_label": "", "object_name": "", "vote": ""}

    def manage_vote(self, modelo: type):
        user = self.request.user
        vote = self.url_info["vote"]
        # TODO the author == user condidition should be inside the vote method
        if modelo.author == user:
            self.error_message = "No puedes votarte a ti mismo"
            raise Exception
        vote_result = modelo.vote(user, vote)
        if vote_result == 0:
            self.error_message = "Ya has votado"
            raise Exception
        return modelo

    def action(self, url_encoded) -> type:
        obj = self.get_object(url_encoded)
        return self.manage_vote(obj)
