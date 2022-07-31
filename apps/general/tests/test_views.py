import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.views import (
MessagesTemplateview,
NotificationsListView,
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestMessagesTemplateview(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNotificationsListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_queryset(self):
        pass
    
