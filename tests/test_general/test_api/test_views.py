from unittest import skip
from unittest.mock import patch

from django.contrib.auth import get_user_model

from bfet import DjangoTestingModel
from rest_framework.test import APITestCase

from src.escritos.models import Term
from src.general.api.views import CreateCommentView, VoteView
from src.preguntas_respuestas.models import Answer, Question


class BaseVoteAndCommentViewTestMixin:
    view_class: type = None  # type: ignore
    notification_type: str = ""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        author = DjangoTestingModel.create(get_user_model())
        cls.term = DjangoTestingModel.create(Term, id=1, slug="slug", author=author)
        cls.question = DjangoTestingModel.create(Question, id=1, slug="slug", author=author)
        cls.answer = DjangoTestingModel.create(
            Answer, id=1, question_related=cls.question, author=author
        )

    def test_build_object(self):
        for app_label, object_name, object_id, expected_result in [
            ("escritos", "term", "1", self.term),
            ("preguntas_respuestas", "answer", "1", self.answer),
            ("preguntas_respuestas", "question", "1", self.question),
        ]:
            with self.subTest(app_label):
                assert expected_result == self.view_class().build_object(
                    app_label, object_name, object_id
                )

    def test_success_url(self):
        for obj, expected_result in [
            (self.term, "/definicion/slug/"),
            (self.question, "/question/slug/"),
            (self.answer, "/question/slug/"),
        ]:
            view = self.view_class()
            view.object = obj
            with self.subTest(obj):
                assert expected_result == view.success_url()

    @skip("not ready")
    @patch("src.notifications.tasks.prepare_notification_task.delay")
    def test_send_notification_and_message(self, mock_prepare_notification_task) -> None:
        for obj in [self.term, self.question, self.answer]:
            self.view_class().send_notification_and_message(obj)
            mock_prepare_notification_task.assert_called_once_with(obj, self.notification_type)
            # messages.success(self.request, self.success_message)

    @skip("not ready")
    @patch("src.notifications.tasks.prepare_notification_task.delay")
    def test_response(self, mock_prepare_notification_task):
        # TODO add encoded url
        for obj in [self.term, self.question, self.answer]:
            with self.subTest("Test error"):
                with self.assertRaises(Exception):
                    # TODO test that message is set
                    pass
            with self.subTest("Test success"):
                self.view_class().response()
                mock_prepare_notification_task.assert_called_once_with(
                    obj, self.notification_type
                )


class TestCreateCommentView(BaseVoteAndCommentViewTestMixin, APITestCase):
    view_class = CreateCommentView

    def test_parse_url(self):
        for obj, expected_result in [
            (self.term, {"id": "1", "app_label": "escritos", "object_name": "Term"}),
            (
                self.question,
                {"id": "1", "app_label": "preguntas_respuestas", "object_name": "Question"},
            ),
            (
                self.answer,
                {"id": "1", "app_label": "preguntas_respuestas", "object_name": "Answer"},
            ),
        ]:
            with self.subTest(obj):
                assert expected_result == self.view_class().parse_url(obj.encoded_url)

    def test_get_object(self):
        for encoded_url, expected_result in [
            (self.term.encoded_url, self.term),
            (self.answer.encoded_url, self.answer),
            (self.question.encoded_url, self.question),
        ]:
            with self.subTest(expected_result):
                assert expected_result == self.view_class().get_object(encoded_url)


class TestVoteView(BaseVoteAndCommentViewTestMixin, APITestCase):
    view_class = VoteView
    encoded_attr: str = "encoded_url"

    def test_parse_url_up(self):
        for obj, expected_result in [
            (
                self.term,
                {
                    "id": "1",
                    "app_label": "escritos",
                    "object_name": "Term",
                    "vote": "up",
                },
            ),
            (
                self.question,
                {
                    "id": "1",
                    "app_label": "preguntas_respuestas",
                    "object_name": "Question",
                    "vote": "up",
                },
            ),
            (
                self.answer,
                {
                    "id": "1",
                    "app_label": "preguntas_respuestas",
                    "object_name": "Answer",
                    "vote": "up",
                },
            ),
        ]:
            with self.subTest(obj):
                assert expected_result == self.view_class().parse_url(obj.base_encoded_url_up)

    def test_parse_url_down(self):
        for obj, expected_result in [
            (
                self.term,
                {
                    "id": "1",
                    "app_label": "escritos",
                    "object_name": "Term",
                    "vote": "down",
                },
            ),
            (
                self.question,
                {
                    "id": "1",
                    "app_label": "preguntas_respuestas",
                    "object_name": "Question",
                    "vote": "down",
                },
            ),
            (
                self.answer,
                {
                    "id": "1",
                    "app_label": "preguntas_respuestas",
                    "object_name": "Answer",
                    "vote": "down",
                },
            ),
        ]:
            with self.subTest(obj):
                assert expected_result == self.view_class().parse_url(
                    obj.base_encoded_url_down
                )

    def test_get_object_upvote(self):
        for encoded_url, expected_result in [
            (self.term.base_encoded_url_up, self.term),
            (self.answer.base_encoded_url_up, self.answer),
            (self.question.base_encoded_url_up, self.question),
        ]:
            with self.subTest(expected_result):
                assert expected_result == self.view_class().get_object(encoded_url)

    def test_get_object_downvote(self):
        for encoded_url, expected_result in [
            (self.term.base_encoded_url_down, self.term),
            (self.answer.base_encoded_url_down, self.answer),
            (self.question.base_encoded_url_down, self.question),
        ]:
            with self.subTest(expected_result):
                assert expected_result == self.view_class().get_object(encoded_url)
