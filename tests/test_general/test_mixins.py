from django.test import TestCase

from bfet import DjangoTestingModel
from apps.escritos.models import Term


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
