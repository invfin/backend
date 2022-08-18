from apps.bfet import ExampleModel

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.general import constants
from apps.general.outils.notifications import NotificationSystem
from apps.general.models import Notification
from apps.public_blog.models import PublicBlog
from apps.preguntas_respuestas.models import Question, Answer

User = get_user_model()


class TestNotificationSystem(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_notify = ExampleModel.create(User)
        cls.writter = ExampleModel.create(User)
        cls.question_author = ExampleModel.create(User)
        cls.answer_author = ExampleModel.create(User)
        cls.blog = ExampleModel.create(PublicBlog, author=cls.writter)
        cls.question = ExampleModel.create(Question, author=cls.question_author)
        cls.answer = ExampleModel.create(Answer, author=cls.answer_author)

    def test_save_notif(self):
        self.assertEqual(0, Notification.objects.all().count())
        email_data = {
            "subject": constants.NEW_FOLLOWER,
            "content": (
                "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones"
            ),
        }
        notif_dict = NotificationSystem().save_notif(
            self.blog,
            self.user_notify,
            constants.NEW_FOLLOWER
        )

    def test_notify(self):
        pass

    def test_announce_new_follower(self):
        pass

    def test_announce_new_comment(self):
        pass

    def test_announce_new_vote(self):
        pass

    def test_announce_new_question(self):
        pass

    def test_announce_new_blog(self):
        pass

    def test_announce_new_answer(self):
        pass

    def test_announce_answer_accepted(self):
        pass

