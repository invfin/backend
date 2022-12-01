from unittest.mock import patch

from rest_framework.test import APITestCase
from bfet import DjangoTestingModel

from django.contrib.auth import get_user_model

from apps.general.api.views import CreateCommentView, VoteView
from apps.escritos.models import Term, TermsComment
from apps.preguntas_respuestas.models import Question, Answer


class BaseVoteAndCommentViewTestMixin(APITestCase):
    view_class: type = None  # type: ignore
    notification_type: str = ""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        author = DjangoTestingModel.create(get_user_model())
        cls.term = DjangoTestingModel.create(Term, id=1, slug="slug", author=author)
        cls.question = DjangoTestingModel.create(Question, id=1, slug="slug", author=author)
        cls.answer = DjangoTestingModel.create(Answer, id=1, question_related=cls.question, author=author)

    def test_get_object(self):
        for app_label, object_name, object_id, expected_result in [
            ("escritos", "term", 1, self.term),
            ("preguntas_respuestas", "answer", 1, self.answer),
            ("preguntas_respuestas", "question", 1, self.question),
        ]:
            with self.subTest(app_label):
                assert expected_result == self.view_class().get_object(app_label, object_name, object_id)

    def test_success_url(self):
        for obj, expected_result in [
            (self.term, "definicion/slug/"),
            (self.question, "question/slug/"),
            (self.answer, "question/slug/"),
        ]:
            view = self.view_class()
            view.object = obj
            with self.subTest(obj):
                assert expected_result == view.success_url()

    @patch("apps.notifications.tasks.prepare_notification_task.delay")
    def test_send_notification_and_message(self, mock_prepare_notification_task) -> None:
        for obj in [self.term, self.question, self.answer]:
            self.view_class().send_notification_and_message(obj)
            mock_prepare_notification_task.assert_called_once_with(obj, self.notification_type)
            # messages.success(self.request, self.success_message)

    @patch("apps.notifications.tasks.prepare_notification_task.delay")
    def test_response(self, mock_prepare_notification_task):
        # TODO add encoded url
        for obj in [self.term, self.question, self.answer]:
            with self.subTest("Test error"):
                with self.assertRaises(Exception):
                    # TODO test that message is set
                    pass
            with self.subTest("Test success"):
                response = self.view_class().response()
                mock_prepare_notification_task.assert_called_once_with(obj, self.notification_type)


class TestCreateCommentView(BaseVoteAndCommentViewTestMixin, APITestCase):
    view_class = CreateCommentView

    def test_parse_url(self):
        for obj, expected_result in [
            (self.term, {"id": 1, "app_label": "escritos", "object_name": "term"}),
            (self.question, {"id": 1, "app_label": "preguntas_respuestas", "object_name": "question"}),
            (self.answer, {"id": 1, "app_label": "preguntas_respuestas", "object_name": "answer"}),
        ]:
            with self.subTest(obj):
                assert expected_result == self.view_class().parse_url(obj.encoded_url_comment)


class TestVoteView(BaseVoteAndCommentViewTestMixin, APITestCase):
    view_class = VoteView

    def test_parse_url(self):
        for obj, expected_result in [
            (self.term, {"id": 1, "app_label": "escritos", "object_name": "term", "vote": 0}),
            (self.question, {"id": 1, "app_label": "preguntas_respuestas", "object_name": "question", "vote": 0}),
            (self.answer, {"id": 1, "app_label": "preguntas_respuestas", "object_name": "answer", "vote": 0}),
        ]:
            with self.subTest(obj):
                assert expected_result == self.view_class().parse_url(obj.encoded_url_comment)
