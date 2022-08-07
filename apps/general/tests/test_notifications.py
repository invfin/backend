from model_bakery import baker

from django.test import TestCase

from apps.general.outils.notifications import NotificationSystem
from apps.general.models import Notification


class TestNotificationSystem(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_save_notif(self):
        pass

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

