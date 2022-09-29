from datetime import datetime, timedelta

import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db

from apps.web.utils import more_than_month


class TestUtils(TestCase):
    def test_more_than_month(self):
        now_less_ten = datetime.now() - timedelta(10)
        self.assertFalse(more_than_month(now_less_ten))

        now_less_twenty = datetime.now() - timedelta(20)
        self.assertFalse(more_than_month(now_less_twenty))

        now_less_thirty = datetime.now() - timedelta(40)
        self.assertTrue(more_than_month(now_less_thirty))
