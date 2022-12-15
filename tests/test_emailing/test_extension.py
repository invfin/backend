from django.test import TestCase

from src.emailing.extensions import EmailExtension


class TestEmailExtension(TestCase):
    def test_email_serialized(self):
        email_extension = EmailExtension()
        email_extension.title = "title"
        email_extension.content = "content"
        email_extension.call_to_action = "call_to_action"
        email_extension.call_to_action_url = "call_to_action_url"
        email_extension.dict_for_task = {"a": "a", "b": "b"}

        assert {
            "subject": "title",
            "content": "content",
            "call_to_action": "call_to_action",
            "call_to_action_url": "call_to_action_url",
            "a": "a",
            "b": "b",
        } == email_extension.email_serialized
