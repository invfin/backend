from apps.bfet import ExampleModel

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.general import constants
from apps.general.outils.notifications import NotificationSystem
from apps.general.models import Notification
from apps.preguntas_respuestas.models import Question, Answer, QuesitonComment, AnswerComment
from apps.public_blog.models import PublicBlog, NewsletterFollowers


User = get_user_model()


class TestNotificationSystem(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.question = ExampleModel.create(Question, author=ExampleModel.create(User))
        cls.question_comment = ExampleModel.create(
            QuesitonComment,
            content_related=ExampleModel.create(Question),
            author=ExampleModel.create(User)
        )
        cls.answer = ExampleModel.create(Answer, author=ExampleModel.create(User))
        cls.answer_comment = ExampleModel.create(
            AnswerComment,
            author=ExampleModel.create(User),
            content_related=ExampleModel.create(Answer),
        )
        cls.writter = ExampleModel.create(User, is_writter=True)
        cls.followers = ExampleModel.create(NewsletterFollowers, user=cls.writter)
        cls.blog = ExampleModel.create(PublicBlog, author=cls.writter)
        cls.user_1 = ExampleModel.create(User)
        cls.user_2 = ExampleModel.create(User)
        cls.followers.followers.add(cls.user_1)

    def test_save_notif(self):
        self.assertEqual(0, Notification.objects.all().count())
        notif_question = NotificationSystem().save_notif(
            object_related=self.question,
            user=self.user_1,
            notif_type=constants.NEW_QUESTION,
            email_data={
                "subject": "question title",
                "content": "question content"
            },
        )
        first_notif = Notification.objects.all().first()
        self.assertEqual(1, Notification.objects.all().count())
        self.assertEqual("question title", notif_question["subject"])
        self.assertEqual("question content", notif_question["content"])
        self.assertEqual(first_notif.shareable_link, notif_question["url_to_join"])
        self.assertEqual("general", notif_question["app_label"])
        self.assertEqual("notification", notif_question["object_name"])
        self.assertEqual(first_notif.id, notif_question["id"])

        notif_answer = NotificationSystem().save_notif(
            object_related=self.answer,
            user=self.user_1,
            notif_type=constants.NEW_ANSWER,
            email_data={
                "subject": "answer title",
                "content": "answer content"
            },
        )
        second_notif = Notification.objects.all().last()
        self.assertEqual(2, Notification.objects.all().count())
        self.assertEqual("answer title", notif_answer["subject"])
        self.assertEqual("answer content", notif_answer["content"])
        self.assertEqual(second_notif.shareable_link, notif_answer["url_to_join"])
        self.assertEqual("general", notif_answer["app_label"])
        self.assertEqual("notification", notif_answer["object_name"])
        self.assertEqual(second_notif.id, notif_answer["id"])

        notif_blog = NotificationSystem().save_notif(
            object_related=self.blog,
            user=self.user_2,
            notif_type=constants.NEW_BLOG_POST,
            email_data={
                "subject": "blog title",
                "content": "blog content"
            },
        )
        third_notif = Notification.objects.all().last()
        self.assertEqual(3, Notification.objects.all().count())
        self.assertEqual("blog title", notif_blog["subject"])
        self.assertEqual("blog content", notif_blog["content"])
        self.assertEqual(third_notif.shareable_link, notif_blog["url_to_join"])
        self.assertEqual("general", notif_blog["app_label"])
        self.assertEqual("notification", notif_blog["object_name"])
        self.assertEqual(third_notif.id, notif_blog["id"])

    def test_notify(self):
        pass

    def test_announce_new_follower(self):
        announce_new_follower = NotificationSystem().announce_new_follower(
            self.user_1,
            constants.NEW_FOLLOWER
        )
        self.assertEqual(type(announce_new_follower), list)
        self.assertEqual(len(announce_new_follower), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_follower = announce_new_follower[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(constants.NEW_FOLLOWER, announce_new_follower["subject"])
        self.assertEqual(
            "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones",
            announce_new_follower["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_new_follower["url_to_join"])
        self.assertEqual("general", announce_new_follower["app_label"])
        self.assertEqual("notification", announce_new_follower["object_name"])
        self.assertEqual(first_notif.id, announce_new_follower["id"])

    def test_announce_new_comment(self):
        announce_new_comment_question = NotificationSystem().announce_new_comment(
            self.question_comment,
            constants.NEW_COMMENT
        )
        self.assertEqual(type(announce_new_comment_question), list)
        self.assertEqual(len(announce_new_comment_question), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_comment_question = announce_new_comment_question[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(constants.NEW_COMMENT, announce_new_comment_question["subject"])
        self.assertEqual(
            f"{self.question_comment.title} ha recibido un nuevo comentario",
            announce_new_comment_question["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_new_comment_question["url_to_join"])
        self.assertEqual("general", announce_new_comment_question["app_label"])
        self.assertEqual("notification", announce_new_comment_question["object_name"])
        self.assertEqual(first_notif.id, announce_new_comment_question["id"])

        announce_new_comment_answer = NotificationSystem().announce_new_comment(
            self.answer_comment,
            constants.NEW_COMMENT
        )
        self.assertEqual(type(announce_new_comment_answer), list)
        self.assertEqual(len(announce_new_comment_answer), 1)
        self.assertEqual(2, Notification.objects.all().count())
        announce_new_comment_answer = announce_new_comment_answer[0]
        second_notif = Notification.objects.all().last()
        self.assertEqual(constants.NEW_COMMENT, announce_new_comment_answer["subject"])
        self.assertEqual(
            f"{self.answer_comment.title} ha recibido un nuevo comentario",
            announce_new_comment_answer["content"]
        )
        self.assertEqual(second_notif.shareable_link, announce_new_comment_answer["url_to_join"])
        self.assertEqual("general", announce_new_comment_answer["app_label"])
        self.assertEqual("notification", announce_new_comment_answer["object_name"])
        self.assertEqual(second_notif.id, announce_new_comment_answer["id"])

    def test_announce_new_vote(self):
        announce_new_vote_question = NotificationSystem().announce_new_vote(
            self.question,
            constants.NEW_VOTE
        )
        self.assertEqual(type(announce_new_vote_question), list)
        self.assertEqual(len(announce_new_vote_question), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_vote_question = announce_new_vote_question[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(constants.NEW_VOTE, announce_new_vote_question["subject"])
        self.assertEqual(
            f"{self.question.title} ha recibido un nuevo voto",
            announce_new_vote_question["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_new_vote_question["url_to_join"])
        self.assertEqual("general", announce_new_vote_question["app_label"])
        self.assertEqual("notification", announce_new_vote_question["object_name"])
        self.assertEqual(first_notif.id, announce_new_vote_question["id"])

        announce_new_vote_answer = NotificationSystem().announce_new_vote(
            self.answer,
            constants.NEW_VOTE
        )
        self.assertEqual(type(announce_new_vote_answer), list)
        self.assertEqual(len(announce_new_vote_answer), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_vote_answer = announce_new_vote_answer[0]
        second_notif = Notification.objects.all().last()
        self.assertEqual(constants.NEW_VOTE, announce_new_vote_answer["subject"])
        self.assertEqual(
            f"{self.answer.title} ha recibido un nuevo voto",
            announce_new_vote_answer["content"]
        )
        self.assertEqual(second_notif.shareable_link, announce_new_vote_answer["url_to_join"])
        self.assertEqual("general", announce_new_vote_answer["app_label"])
        self.assertEqual("notification", announce_new_vote_answer["object_name"])
        self.assertEqual(second_notif.id, announce_new_vote_answer["id"])

    def test_announce_new_question(self):
        announce_new_question = NotificationSystem().announce_new_question(
            self.question,
            constants.NEW_QUESTION
        )
        self.assertEqual(type(announce_new_question), list)
        self.assertEqual(len(announce_new_question), User.objects.all().exclude(pk=self.question.author.pk).count())
        self.assertEqual(User.objects.all().exclude(pk=self.question.author.pk).count(), Notification.objects.all().count())
        announce_new_question = announce_new_question[0]
        first_notif = Notification.objects.all().first()
        title = self.question.title[:15]
        self.assertEqual(
            f"{constants.NEW_QUESTION} {title}...",
            announce_new_question["subject"]
        )
        self.assertEqual(
            self.question.content,
            announce_new_question["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_new_question["url_to_join"])
        self.assertEqual("general", announce_new_question["app_label"])
        self.assertEqual("notification", announce_new_question["object_name"])
        self.assertEqual(first_notif.id, announce_new_question["id"])

    def test_announce_new_blog(self):
        announce_new_blog = NotificationSystem().announce_new_blog(
            self.blog,
            constants.NEW_BLOG_POST
        )
        self.assertEqual(type(announce_new_blog), list)
        self.assertEqual(len(announce_new_blog), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_blog = announce_new_blog[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(self.blog.title, announce_new_blog["subject"])
        self.assertEqual(self.blog.content, announce_new_blog["content"])
        self.assertEqual(first_notif.shareable_link, announce_new_blog["url_to_join"])
        self.assertEqual("general", announce_new_blog["app_label"])
        self.assertEqual("notification", announce_new_blog["object_name"])
        self.assertEqual(first_notif.id, announce_new_blog["id"])

    def test_announce_new_answer(self):
        announce_new_answer = NotificationSystem().announce_new_answer(
            self.answer,
            constants.NEW_ANSWER
        )
        self.assertEqual(type(announce_new_answer), list)
        self.assertEqual(len(announce_new_answer), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_new_answer = announce_new_answer[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(constants.NEW_FOLLOWER, announce_new_answer["subject"])
        self.assertEqual(
            "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones",
            announce_new_answer["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_new_answer["url_to_join"])
        self.assertEqual("general", announce_new_answer["app_label"])
        self.assertEqual("notification", announce_new_answer["object_name"])
        self.assertEqual(first_notif.id, announce_new_answer["id"])

    def test_announce_answer_accepted(self):
        announce_answer_accepted = NotificationSystem().announce_answer_accepted(
            self.answer,
            constants.ANSWER_ACCEPTED
        )
        self.assertEqual(type(announce_answer_accepted), list)
        self.assertEqual(len(announce_answer_accepted), 1)
        self.assertEqual(1, Notification.objects.all().count())
        announce_answer_accepted = announce_answer_accepted[0]
        first_notif = Notification.objects.all().first()
        self.assertEqual(constants.NEW_FOLLOWER, announce_answer_accepted["subject"])
        self.assertEqual(
            "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones",
            announce_answer_accepted["content"]
        )
        self.assertEqual(first_notif.shareable_link, announce_answer_accepted["url_to_join"])
        self.assertEqual("general", announce_answer_accepted["app_label"])
        self.assertEqual("notification", announce_answer_accepted["object_name"])
        self.assertEqual(first_notif.id, announce_answer_accepted["id"])

