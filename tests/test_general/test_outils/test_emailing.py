from django.core import mail
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from bfet import DjangoTestingModel

from apps.general.outils.emailing import EmailingSystem
from apps.escritos.models import Term
from apps.general import constants

User = get_user_model()


class EmailTest(TestCase):
    @override_settings(
        EMAIL_CONTACT = "contact@invfin.xyz",
        MAIN_EMAIL = "main@invfin.xyz",
        EMAIL_ACCOUNTS = "accounts@invfin.xyz",
        EMAIL_SUGGESTIONS = "suggestion@invfin.xyz",
        EMAIL_DEFAULT = "default@invfin.xyz",
    )
    def setUp(self) -> None:
        self.emailing_sys = EmailingSystem

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User)
        cls.term = DjangoTestingModel.create(Term)

    def test__prepare_email_track(self):
        term.dict_for_task
        self.emailing_sys()._prepare_email_track()

    def test__prepare_email(self, email: Dict[str, str], receiver: User) -> Tuple[str, str]:
        sender = self._prepare_sender(email.pop("sender", None))
        message = self.prepare_message(email, receiver)
        return message, sender

    def test__prepare_sender(self, sender: str = None) -> str:
        self.emailing_sys()._prepare_sender()
        if self.is_for == constants.EMAIL_FOR_PUBLIC_BLOG:
            email = settings.EMAIL_NEWSLETTER
        elif self.is_for == constants.EMAIL_FOR_NOTIFICATION:
            email = settings.EMAIL_DEFAULT
            sender = "InvFin"
        else:
            email = settings.MAIN_EMAIL
            sender = "Lucas - InvFin"

        return f"{sender} <{email}>"

    def test_prepare_message(self, email: Dict[str, str], receiver: User) -> str:
        base_message = {**email, "user": receiver, "image_tag": self._prepare_email_track(email, receiver)}
        return render_to_string(self.email_template, base_message)

    def test_enviar_email(self, email: Dict, receiver_id: int):
        receiver = User.objects.get(id=receiver_id)
        subject = email.pop("subject")
        message, sender = self._prepare_email(email, receiver)

        email_message = EmailMessage(subject, message, sender, [receiver.email])

        email_message.content_subtype = "html"
        email_message.send()

    def test_simple_email(self):
        subject, message = "Subject here", "Message there"
        self.emailing_sys.simple_email(subject, message, settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Subject here'
        assert mail.outbox[0].message == 'Message there'
        assert mail.outbox[0].from_email == 'default@invfin.xyz'
        assert mail.outbox[0].recipient_list == ["default@invfin.xyz"]
