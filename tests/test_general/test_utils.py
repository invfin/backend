from django.test import TestCase, override_settings

from bfet import DjangoTestingModel

from src.general.constants import BUSINESS_SUBDOMAIN
from src.general.utils import HostChecker
from src.public_blog.models import WriterProfile
from src.users.models import User


class MockRequest:
    def __init__(self, host: str):
        self.host = host

    def get_host(self):
        return f"{self.host}.current.com"


class TestHostChecker(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.request = MockRequest("host_name")
        cls.business_request = MockRequest(BUSINESS_SUBDOMAIN)
        cls.user = DjangoTestingModel.create(User)
        cls.writer = DjangoTestingModel.create(
            WriterProfile,
            user=cls.user,
            host_name="host_name",
        )

    def test_get_host(self):
        assert HostChecker(self.request).get_host() == "host_name"
        assert HostChecker(self.business_request).get_host() == "business"

    def test_get_writer(self):
        assert HostChecker(self.business_request).get_writer() is None
        assert HostChecker(self.request).get_writer() == self.writer

    def test_return_user_writer(self):
        assert HostChecker(self.business_request).return_user_writer() is None
        assert HostChecker(self.request).return_user_writer() == self.user

    def test_host_is_business(self):
        assert HostChecker(self.business_request).host_is_business() is True
        assert HostChecker(self.request).host_is_business() is False

    @override_settings(CURRENT_DOMAIN="current.com")
    def test_current_site_domain(self):
        assert HostChecker(self.request).current_site_domain() == "current.com"
