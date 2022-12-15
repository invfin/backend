from django.test import TestCase

from bfet import DjangoTestingModel

from src.users.models import User
from src.escritos.models import Term
from src.preguntas_respuestas.models import Question
from src.general.mixins import VotesMixin


class TestMixins(TestCase):
    def test_save_unique_field(self):
        term = DjangoTestingModel.create(Term)
        unique = term.save_unique_field("slug", "algo raro")
        assert unique == "algo-raro"
        unique = term.save_unique_field("slug", "algo raro", extra="papa")
        assert unique == "algo-raro-papa"
        unique = term.save_unique_field("slug", "algo raro", extra="pa pa")
        assert unique == "algo-raro-pa-pa"
        term_2 = DjangoTestingModel.create(Term, slug="nada")
        unique_2 = term_2.save_unique_field("slug", "nada")
        assert unique_2 == "nada-1"
        term_3 = DjangoTestingModel.create(Term, slug="nada-1")
        unique_3 = term_3.save_unique_field("slug", "nada")
        assert unique_3 == "nada-2"


class TestBaseToAllMixin(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term = DjangoTestingModel.create(Term)

    def test_build_admin_url(self):
        for admin_action, admin_path in [
            ("changelist", "/admin/escritos/term/"),
            ("add", "/admin/escritos/term/add/"),
            ("history", f"/admin/escritos/term/{self.term.id}/history/"),
            ("delete", f"/admin/escritos/term/{self.term.id}/delete/"),
            ("change", f"/admin/escritos/term/{self.term.id}/change/"),
        ]:
            with self.subTest(admin_action):
                full_admin_url = self.term.build_admin_url(admin_action)
                built_admin_path = self.term.build_admin_url(admin_action, False)
                assert admin_path == built_admin_path
                assert full_admin_url.startswith("http://example.com:8000") is True
                assert f"http://example.com:8000{admin_path}" == full_admin_url

    def test_admin_urls(self):
        expected_result = {
            "changelist": "http://example.com:8000/admin/escritos/term/",
            "add": "http://example.com:8000/admin/escritos/term/add/",
            "history": f"http://example.com:8000/admin/escritos/term/{self.term.id}/history/",
            "delete": f"http://example.com:8000/admin/escritos/term/{self.term.id}/delete/",
            "change": f"http://example.com:8000/admin/escritos/term/{self.term.id}/change/",
        }
        assert expected_result == self.term.admin_urls


class TestVotesMixin(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = DjangoTestingModel.create(User)
        cls.user_2 = DjangoTestingModel.create(User)
        cls.question = DjangoTestingModel.create(Question, author=DjangoTestingModel.create(User))
        cls.question.upvotes.add(cls.user_1)
        cls.question.downvotes.add(cls.user_2)

    def test_action_is_upvote(self):
        assert VotesMixin.action_is_upvote("up") is True
        assert VotesMixin.action_is_upvote("down") is False
    
    def test_action_is_downvote(self):
        assert VotesMixin.action_is_downvote("down") is True
        assert VotesMixin.action_is_downvote("up") is False
    
    def test_user_already_upvoted(self):
        assert self.question.user_already_upvoted(self.user_1) is True
        assert self.question.user_already_upvoted(self.user_2) is False
    
    def test_user_already_downvoted(self):
        assert self.question.user_already_downvoted(self.user_2) is True
        assert self.question.user_already_downvoted(self.user_1) is False
    