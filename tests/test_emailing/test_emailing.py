from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from bfet import DjangoTestingModel

from src.emailing import constants
from src.emailing.outils.emailing import EmailingSystem
from src.web.models import WebsiteEmail, WebsiteEmailTrack

User = get_user_model()


class EmailTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User, first_name="f", last_name="f", email="test@user.com")

    def test_html_link(self):
        assert '<a href="link" target="_blank">Text</a>' == EmailingSystem.html_link("link", "Text")
        assert '<a href="http://example.com:8000link" target="_blank">Text</a>' == EmailingSystem.html_link(
            "link", "Text", True
        )

    def test__prepare_email_track(self):
        web_email = DjangoTestingModel.create(WebsiteEmail, id=1)
        email_info_image_tag_tracker = {
            "app_label": "web",
            "object_name": "WebsiteEmail",
            "id": 1,
        }
        email_machine_response = EmailingSystem()._prepare_email_track(email_info_image_tag_tracker, self.user)
        web_email_track = WebsiteEmailTrack.objects.get(email_related=web_email)
        assert web_email_track.encoded_url == email_machine_response
        assert self.user == web_email_track.sent_to

    def test__prepare_email(self):
        web_email = DjangoTestingModel.create(WebsiteEmail, id=1)
        email_info_image_tag_tracker = {
            "app_label": "web",
            "object_name": "WebsiteEmail",
            "id": 1,
        }
        email_dict = {
            "subject": "Subject here",
            "sender": "EMAIL_DEFAULT@example.com",  # Not always necessary
            **email_info_image_tag_tracker,
        }
        sender, message = EmailingSystem(constants.EMAIL_FOR_NOTIFICATION)._prepare_email(email_dict, self.user)
        email_track = WebsiteEmailTrack.objects.get(email_related=web_email)
        expected_data = {
            "subject": "Subject here",
            "call_to_action": "",
            "call_to_action_url": "",
            "user": self.user,
            "image_tag": email_track.encoded_url,
        }
        assert "InvFin <EMAIL_DEFAULT@example.com>" == sender
        assert expected_data == message

    def test__prepare_sender(self):
        """
        TODO test it with all the web objectives
        """
        public_blog_sender = EmailingSystem(constants.EMAIL_FOR_PUBLIC_BLOG)._prepare_sender("writter")
        notif_sender = EmailingSystem(constants.EMAIL_FOR_NOTIFICATION)._prepare_sender()
        web_sender = EmailingSystem(constants.EMAIL_FOR_WEB, "Not in web objective")._prepare_sender()
        assert "writter <EMAIL_NEWSLETTER@example.com>" == public_blog_sender
        assert "InvFin <EMAIL_DEFAULT@example.com>" == notif_sender
        assert "Lucas - InvFin <MAIN_EMAIL@example.com>" == web_sender

    def test__prepare_call_to_action(self):
        data = {
            "call_to_action": "call_to_action",
            "call_to_action_url": "call_to_action_url",
        }
        expected_result = {
            "call_to_action": "call_to_action",
            "call_to_action_url": "call_to_action_url",
        }
        assert expected_result == EmailingSystem(constants.EMAIL_FOR_NOTIFICATION)._prepare_call_to_action(data)

        data = {"call_to_action": "", "call_to_action_url": ""}
        expected_result = {"call_to_action": "", "call_to_action_url": ""}
        assert expected_result == EmailingSystem(constants.EMAIL_FOR_NOTIFICATION)._prepare_call_to_action(data)

    def test__prepare_content(self):
        email_machine = EmailingSystem(constants.EMAIL_FOR_NOTIFICATION)
        web_email = DjangoTestingModel.create(WebsiteEmail, id=1)
        email_info_image_tag_tracker = {
            "app_label": "web",
            "object_name": "WebsiteEmail",
            "id": 1,
        }
        email_dict = {
            "subject": "Subject here",
            "sender": "EMAIL_DEFAULT@example.com",  # Not always necessary
            **email_info_image_tag_tracker,
        }
        email_machine_response = email_machine._prepare_content(email_dict, self.user)
        email_track = WebsiteEmailTrack.objects.get(email_related=web_email)
        expected_result = {
            "subject": "Subject here",
            "sender": "EMAIL_DEFAULT@example.com",
            "user": self.user,
            "call_to_action": "",
            "call_to_action_url": "",
            "image_tag": email_track.encoded_url,
        }
        assert expected_result == email_machine_response

    def test_rich_email(self):
        DjangoTestingModel.create(WebsiteEmail, id=1)
        email_info_image_tag_tracker = {
            "app_label": "web",
            "object_name": "WebsiteEmail",
            "id": 1,
        }
        email_dict = {
            "subject": "Subject here",
            "message": "Message there",
            "sender": "EMAIL_DEFAULT@example.com",  # Not always necessary
            **email_info_image_tag_tracker,
        }
        # Need to check all the posibilities for EMAIL_FOR and purpose
        EmailingSystem(constants.EMAIL_FOR_NOTIFICATION).rich_email(email_dict, self.user.id)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Subject here"
        # assert mail.outbox[0].body == 'Message there' Improve the parsing of the body to test it
        assert mail.outbox[0].from_email == "InvFin <EMAIL_DEFAULT@example.com>"
        assert mail.outbox[0].to == ["test@user.com"]

    def test_simple_email(self):
        subject, message = "Subject here", "Message there"
        EmailingSystem.simple_email(subject, message)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Subject here"
        # assert mail.outbox[0].body == TODO find how to test the field
        assert mail.outbox[0].from_email == "Web-automation <EMAIL_DEFAULT@example.com>"
        assert mail.outbox[0].to == ["EMAIL_DEFAULT@example.com"]
