import time
from typing import Callable, Dict, List, Tuple, Union

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Q

from src.emailing.constants import EMAIL_FOR_NOTIFICATION
from src.notifications import constants
from src.notifications.models import Notification

User = get_user_model()


class NotificationSystem:
    """
    new_blog_post    -----> followers
    new_comment      -----> related
    new_vote         -----> single
    new_follower     -----> sinlge
    new_question     -----> all
    new_answer       -----> related
    answer_accepted  -----> related
    purchase_successful-----> sinlge

    The annonunce_ method return a list 'cause on the task we iterate over the emails to send
    """

    @classmethod
    def save_notif(cls, object_related, user, notif_type, email_data):
        notification = Notification.objects.create(
            user=user,
            object=object_related,
            notification_type=notif_type,
        )
        return {
            **email_data,
            "url_to_join": object_related.shareable_link,
            "app_label": notification.app_label,
            "object_name": notification.object_name,
            "id": notification.pk,
            "call_to_action_url": object_related.shareable_link,
        }

    @staticmethod
    def get_object_related_params(object_related_dict: Dict) -> Tuple:
        app_label = object_related_dict.pop("app_label")
        object_name = object_related_dict.pop("object_name")
        pk = object_related_dict.pop("id")
        return app_label, object_name, pk

    @staticmethod
    def get_object_related_model(app_label, object_name) -> type:
        return apps.get_model(app_label, object_name, require_ready=True)

    @classmethod
    def get_object_related(cls, object_related_dict: Dict) -> type:
        app_label, object_name, pk = cls.get_object_related_params(object_related_dict)
        model = cls.get_object_related_model(app_label, object_name)
        return model._default_manager.get(pk=pk)

    @classmethod
    def get_notification_method(cls, notif_type: str) -> Callable:
        notif_type_fnct = {
            constants.NEW_BLOG_POST: cls.announce_new_blog,
            constants.NEW_COMMENT: cls.announce_new_comment,
            constants.NEW_VOTE: cls.announce_new_vote,
            constants.NEW_FOLLOWER: cls.announce_new_follower,
            constants.NEW_QUESTION: cls.announce_new_question,
            constants.NEW_ANSWER: cls.announce_new_answer,
            constants.ANSWER_ACCEPTED: cls.announce_answer_accepted,
        }
        return notif_type_fnct[notif_type]

    @classmethod
    def notify(cls, object_related_dict: Dict, notif_type: str) -> List:
        time.sleep(10)
        object_related = cls.get_object_related(object_related_dict)
        notification_fnct = cls.get_notification_method(notif_type)
        return notification_fnct(object_related, notif_type)

    @staticmethod
    def prepare_notification_dict(email: Dict, receiver_id: int) -> Dict[str, Union[Dict, int, str]]:
        return {
            "email": email,
            "receiver_id": receiver_id,
            "is_for": EMAIL_FOR_NOTIFICATION,
        }

    @classmethod
    def announce_new_follower(cls, writer, notif_type):
        return [
            {
                "email": cls.save_notif(
                    writer,
                    writer,
                    notif_type,
                    {
                        "subject": constants.NEW_FOLLOWER,
                        "content": (
                            "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día,"
                            " felicitaciones"
                        ),
                    },
                ),
                "receiver_id": writer.id,
                "is_for": EMAIL_FOR_NOTIFICATION,
            }
        ]

    @classmethod
    def announce_new_comment(cls, obj, notif_type):
        return [
            {
                "email": cls.save_notif(
                    obj,
                    obj.content_related.author,
                    notif_type,
                    {
                        "subject": constants.NEW_COMMENT,
                        "content": f"{obj.content_related.title} ha recibido un nuevo comentario",
                    },
                ),
                "receiver_id": obj.content_related.author.id,
                "is_for": EMAIL_FOR_NOTIFICATION,
            }
        ]

    @classmethod
    def announce_new_vote(cls, obj, notif_type):
        return [
            {
                "email": cls.save_notif(
                    obj,
                    obj.author,
                    notif_type,
                    {
                        "subject": constants.NEW_VOTE,
                        "content": f"{obj.title} ha recibido un nuevo voto",
                    },
                ),
                "receiver_id": obj.author.id,
                "is_for": EMAIL_FOR_NOTIFICATION,
            }
        ]

    @classmethod
    def announce_new_question(cls, question, notif_type):
        notif_info = []
        for user in User.objects.exclude(Q(pk=question.author.pk) | Q(is_bot=True)):
            title = question.title[:15]
            subject = f"{constants.NEW_QUESTION} {title}..."
            email = cls.save_notif(
                question,
                user,
                notif_type,
                {
                    "subject": subject,
                    "content": f"Hay una nueva pregunta: \n{question.content}\n ¿Conoces la respuesta?",
                    "call_to_action": "Se el primero en ayudar y gana créditos extras",
                },
            )
            notif_info.append(cls.prepare_notification_dict(email, user.id))
        return notif_info

    @classmethod
    def announce_new_blog(cls, blog, notif_type):
        # blog.author.main_writer_followed.followers.all()
        # that should be the actual loop over, all the writer's followers
        notif_info = []
        for user in blog.author.main_writer_followed.followers.exclude(is_bot=True):
            email = cls.save_notif(
                blog,
                user,
                notif_type,
                {
                    "subject": blog.title,
                    "content": blog.resume,
                },
            )
            notif_info.append(cls.prepare_notification_dict(email, user.id))
        return notif_info

    @classmethod
    def announce_new_answer(cls, answer, notif_type):
        notif_info = []
        question = answer.question_related
        users_relateds = question.related_users
        users_relateds.append(question.author)
        for user in users_relateds:
            if user != answer.author:
                title = question.title[:15]
                subject = f"{title}... tiene una nueva respuesta"
                if question.author == user:
                    subject = "Tu pregunta tiene una nueva respuesta"
                email = cls.save_notif(
                    answer,
                    user,
                    notif_type,
                    {
                        "subject": subject,
                        "content": answer.content,
                    },
                )
                notif_info.append(cls.prepare_notification_dict(email, user.id))

        return notif_info

    @classmethod
    def announce_answer_accepted(cls, answer, notif_type):
        notif_info = []
        question = answer.question_related
        for user in question.related_users:
            title = question.title[:15]
            subject = f"{title}... tiene una respuesta acceptada"
            content = f"No te lo pierdas, {question.title} ya tiene una respuesta acceptda."
            if answer.author == user:
                subject = "Tu respuesta ha sido acceptada"
                content = f"Felicidades. Tu respuesta a {question.title} ha sido acceptda."
            email = cls.save_notif(
                answer,
                user,
                notif_type,
                {
                    "subject": subject,
                    "content": content,
                },
            )
            notif_info.append(cls.prepare_notification_dict(email, user.id))
        return notif_info
