from typing import Any, Dict

from rest_framework.views import APIView

from src.notifications import constants

from .mixins import BaseVoteAndCommentMixin


class CreateCommentView(BaseVoteAndCommentMixin, APIView):
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


class VoteView(BaseVoteAndCommentMixin, APIView):
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
