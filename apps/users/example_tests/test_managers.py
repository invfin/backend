import vcr
from model_bakery import baker

import pytest

from django.test import TestCase


from apps.users.managers import (
    CreditHistorialManager,
    ProfileManager,
    UserExtraManager,
)

users_vcr = vcr.VCR(
    cassette_library_dir="cassettes/users/managers/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@pytest.mark.django_db
class TestCreditHistorialManager:
    @classmethod
    def setup_class(cls):
        pass

    def test_check_enought_credits(self):
        pass

    def test_update_credits(self):
        pass


@pytest.mark.django_db
class TestProfileManager:
    @classmethod
    def setup_class(cls):
        pass

    def test_create_ref_code(self):
        pass


@pytest.mark.django_db
class TestUserExtraManager:
    @classmethod
    def setup_class(cls):
        pass

    def test_get_or_create_quick_user(self):
        pass
