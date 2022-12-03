import vcr
from model_bakery import baker

import pytest

from django.test import TestCase


from src.users.managers import (
    CreditHistorialManager,
    ProfileManager,
    UserExtraManager,
)

users_vcr = vcr.VCR(
    cassette_library_dir="cassettes/users/managers/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


from django.test import TestCase


class TestCreditHistorialManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_check_enought_credits(self):
        pass

    def test_update_credits(self):
        pass


from django.test import TestCase


class TestProfileManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_create_ref_code(self):
        pass


from django.test import TestCase


class TestUserExtraManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_or_create_quick_user(self):
        pass
