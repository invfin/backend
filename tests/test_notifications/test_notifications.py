from django.test import TestCase

from bfet import DjangoTestingModel

from django.contrib.auth import get_user_model

from apps.notifications import constants
from apps.notifications.outils.notifications import NotificationSystem
from apps.notifications.models import Notification
from apps.users.models import Profile
from apps.preguntas_respuestas.models import Question, QuesitonComment, AnswerComment, Answer
from apps.public_blog.models import PublicBlog, NewsletterFollowers

User = get_user_model()


class TestNotificationSystem(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.writter = DjangoTestingModel.create(User, is_writter=True)
        cls.user_1 = DjangoTestingModel.create(User, first_name="question", last_name="author")
        cls.user_2 = DjangoTestingModel.create(User)
        DjangoTestingModel.create(Profile, user=cls.writter)
        DjangoTestingModel.create(Profile, user=cls.user_1)
        DjangoTestingModel.create(Profile, user=cls.user_2)
        cls.question = DjangoTestingModel.create(Question, author=cls.user_1)
        cls.question_comment = DjangoTestingModel.create(
            QuesitonComment,
            content_related=DjangoTestingModel.create(
                Question,
                author=DjangoTestingModel.create(User),
            ),
            author=DjangoTestingModel.create(User),
        )
        cls.answer = DjangoTestingModel.create(
            Answer,
            author=DjangoTestingModel.create(
                User,
                first_name="answer",
                last_name="author",
            ),
            question_related=cls.question,
        )
        cls.answer_comment = DjangoTestingModel.create(
            AnswerComment,
            author=DjangoTestingModel.create(User),
            content_related=DjangoTestingModel.create(
                Answer,
                author=DjangoTestingModel.create(User),
                question_related=DjangoTestingModel.create(Question, author=DjangoTestingModel.create(User)),
            ),
        )
        cls.followers = DjangoTestingModel.create(NewsletterFollowers, user=cls.writter)
        cls.blog = DjangoTestingModel.create(PublicBlog, author=cls.writter)
        cls.followers.followers.add(cls.user_1)

    def test_save_notif(self):
        assert 0 == Notification.objects.all().count()
        notif_question = NotificationSystem().save_notif(
            object_related=self.question,
            user=self.user_1,
            notif_type=constants.NEW_QUESTION,
            email_data={"subject": "question title", "content": "question content"},
        )
        first_notif = Notification.objects.all().first()
        first_notif.refresh_from_db()
        assert first_notif.object == self.question
        assert 1 == Notification.objects.all().count()
        assert "question title" == notif_question["subject"]
        assert "question content" == notif_question["content"]
        assert first_notif.object.shareable_link == notif_question["url_to_join"]
        assert "notifications" == notif_question["app_label"]
        assert "Notification" == notif_question["object_name"]
        assert first_notif.id == notif_question["id"]

        notif_answer = NotificationSystem().save_notif(
            object_related=self.answer,
            user=self.user_1,
            notif_type=constants.NEW_ANSWER,
            email_data={"subject": "answer title", "content": "answer content"},
        )
        second_notif = Notification.objects.all().last()
        assert 2 == Notification.objects.all().count()
        assert "answer title" == notif_answer["subject"]
        assert "answer content" == notif_answer["content"]
        assert self.answer.shareable_link == notif_answer["url_to_join"]
        assert "notifications" == notif_answer["app_label"]
        assert "Notification" == notif_answer["object_name"]
        assert second_notif.id == notif_answer["id"]

        notif_blog = NotificationSystem().save_notif(
            object_related=self.blog,
            user=self.user_2,
            notif_type=constants.NEW_BLOG_POST,
            email_data={"subject": "blog title", "content": "blog content"},
        )
        third_notif = Notification.objects.all().last()
        assert 3 == Notification.objects.all().count()
        assert "blog title" == notif_blog["subject"]
        assert "blog content" == notif_blog["content"]
        assert self.blog.shareable_link == notif_blog["url_to_join"]
        assert "notifications" == notif_blog["app_label"]
        assert "Notification" == notif_blog["object_name"]
        assert third_notif.id == notif_blog["id"]

    def test_announce_new_follower(self):
        announce_new_follower = NotificationSystem().announce_new_follower(self.user_1, constants.NEW_FOLLOWER)
        assert type(announce_new_follower) == list
        assert len(announce_new_follower) == 1
        assert 1 == Notification.objects.all().count()
        announce_new_follower = announce_new_follower[0]["email"]
        first_notif = Notification.objects.all().first()
        assert constants.NEW_FOLLOWER == announce_new_follower["subject"]
        assert (
            "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones"
            == announce_new_follower["content"]
        )
        assert self.user_1.shareable_link == announce_new_follower["url_to_join"]
        assert "notifications" == announce_new_follower["app_label"]
        assert "Notification" == announce_new_follower["object_name"]
        assert first_notif.id == announce_new_follower["id"]

    def test_announce_new_comment(self):
        announce_new_comment_question = NotificationSystem().announce_new_comment(
            self.question_comment, constants.NEW_COMMENT
        )
        assert type(announce_new_comment_question) == list
        assert len(announce_new_comment_question) == 1
        assert 1 == Notification.objects.all().count()
        announce_new_comment_question = announce_new_comment_question[0]["email"]
        first_notif = Notification.objects.all().first()
        assert constants.NEW_COMMENT == announce_new_comment_question["subject"]
        assert (
            f"{self.question_comment.title} ha recibido un nuevo comentario" == announce_new_comment_question["content"]
        )
        assert self.question_comment.shareable_link == announce_new_comment_question["url_to_join"]
        assert "notifications" == announce_new_comment_question["app_label"]
        assert "Notification" == announce_new_comment_question["object_name"]
        assert first_notif.id == announce_new_comment_question["id"]

        announce_new_comment_answer = NotificationSystem().announce_new_comment(
            self.answer_comment, constants.NEW_COMMENT
        )
        assert type(announce_new_comment_answer) == list
        assert len(announce_new_comment_answer) == 1
        assert 2 == Notification.objects.all().count()
        announce_new_comment_answer = announce_new_comment_answer[0]["email"]
        second_notif = Notification.objects.all().last()
        assert constants.NEW_COMMENT == announce_new_comment_answer["subject"]
        assert f"{self.answer_comment.title} ha recibido un nuevo comentario" == announce_new_comment_answer["content"]
        assert self.answer_comment.shareable_link == announce_new_comment_answer["url_to_join"]
        assert "notifications" == announce_new_comment_answer["app_label"]
        assert "Notification" == announce_new_comment_answer["object_name"]
        assert second_notif.id == announce_new_comment_answer["id"]

    def test_announce_new_vote(self):
        announce_new_vote_question = NotificationSystem().announce_new_vote(self.question, constants.NEW_VOTE)
        assert type(announce_new_vote_question) == list
        assert len(announce_new_vote_question) == 1
        assert 1 == Notification.objects.all().count()
        announce_new_vote_question = announce_new_vote_question[0]["email"]
        first_notif = Notification.objects.all().first()
        assert constants.NEW_VOTE == announce_new_vote_question["subject"]
        assert f"{self.question.title} ha recibido un nuevo voto" == announce_new_vote_question["content"]
        assert self.question.shareable_link == announce_new_vote_question["url_to_join"]
        assert "notifications" == announce_new_vote_question["app_label"]
        assert "Notification" == announce_new_vote_question["object_name"]
        assert first_notif.id == announce_new_vote_question["id"]

        announce_new_vote_answer = NotificationSystem().announce_new_vote(self.answer, constants.NEW_VOTE)
        assert type(announce_new_vote_answer) == list
        assert len(announce_new_vote_answer) == 1
        assert 2 == Notification.objects.all().count()
        announce_new_vote_answer = announce_new_vote_answer[0]["email"]
        second_notif = Notification.objects.all().last()
        assert constants.NEW_VOTE == announce_new_vote_answer["subject"]
        assert f"{self.answer.title} ha recibido un nuevo voto" == announce_new_vote_answer["content"]
        assert self.answer.shareable_link == announce_new_vote_answer["url_to_join"]
        assert "notifications" == announce_new_vote_answer["app_label"]
        assert "Notification" == announce_new_vote_answer["object_name"]
        assert second_notif.id == announce_new_vote_answer["id"]

    def test_announce_new_question(self):
        announce_new_question = NotificationSystem().announce_new_question(self.question, constants.NEW_QUESTION)
        assert type(announce_new_question) == list
        assert len(announce_new_question) == User.objects.all().exclude(pk=self.question.author.pk).count()
        assert User.objects.all().exclude(pk=self.question.author.pk).count() == Notification.objects.all().count()
        announce_new_question = announce_new_question[0]["email"]
        first_notif = Notification.objects.all().first()
        title = self.question.title[:15]
        assert f"{constants.NEW_QUESTION} {title}..." == announce_new_question["subject"]
        assert self.question.content == announce_new_question["content"]
        assert self.question.shareable_link == announce_new_question["url_to_join"]
        assert "notifications" == announce_new_question["app_label"]
        assert "Notification" == announce_new_question["object_name"]
        assert first_notif.id == announce_new_question["id"]

    def test_announce_new_blog(self):
        announce_new_blog = NotificationSystem().announce_new_blog(self.blog, constants.NEW_BLOG_POST)
        assert type(announce_new_blog) == list
        assert len(announce_new_blog) == 2
        assert 2 == Notification.objects.all().count()
        announce_new_blog = announce_new_blog[0]["email"]
        first_notif = Notification.objects.all().first()
        assert self.blog.title == announce_new_blog["subject"]
        assert self.blog.content == announce_new_blog["content"]
        assert self.blog.shareable_link == announce_new_blog["url_to_join"]
        assert "notifications" == announce_new_blog["app_label"]
        assert "Notification" == announce_new_blog["object_name"]
        assert first_notif.id == announce_new_blog["id"]

    def test_announce_new_answer(self):
        announce_new_answer = NotificationSystem().announce_new_answer(self.answer, constants.NEW_ANSWER)
        assert isinstance(announce_new_answer, list)
        assert len(announce_new_answer) == 2
        assert 2 == Notification.objects.all().count()
        announce_new_answer = announce_new_answer[0]["email"]
        first_notif = Notification.objects.all().first()
        assert "Tu pregunta tiene una nueva respuesta" == announce_new_answer["subject"]
        assert self.answer.content == announce_new_answer["content"]
        assert self.answer.shareable_link == announce_new_answer["url_to_join"]
        assert "notifications" == announce_new_answer["app_label"]
        assert "Notification" == announce_new_answer["object_name"]
        assert first_notif.id == announce_new_answer["id"]

    def test_announce_answer_accepted(self):
        announce_answer_accepted = NotificationSystem().announce_answer_accepted(self.answer, constants.ANSWER_ACCEPTED)
        assert type(announce_answer_accepted) == list
        assert len(announce_answer_accepted) == 2
        assert 2 == Notification.objects.all().count()
        announce_answer_accepted = announce_answer_accepted[0]["email"]
        first_notif = Notification.objects.filter(user__first_name="answer").first()
        assert "Tu respuesta ha sido acceptada" == announce_answer_accepted["subject"]
        assert (
            f"Tu respuesta a {self.answer.question_related.title} ha sido acceptda. Felicidades."
            == announce_answer_accepted["content"]
        )
        assert self.answer.shareable_link == announce_answer_accepted["url_to_join"]
        assert "notifications" == announce_answer_accepted["app_label"]
        assert "Notification" == announce_answer_accepted["object_name"]
        assert first_notif.id == announce_answer_accepted["id"]
