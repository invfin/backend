from typing import Dict

import time

from django.apps import apps
from django.contrib.auth import get_user_model

from apps.general import constants
from apps.general.models import Notification

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
    """
    def save_notif(self, object_related, user, notif_type, email_data):

        notification = Notification.objects.create(
        user = user,
        object = object_related,
        notification_type = notif_type,
        )
        return {
            **email_data,
            'url_to_join': object_related.shareable_link,
            'app_label': notification.app_label,
            'object_name': notification.object_name,
            'id': notification.pk
        }

    @classmethod
    def notify(cls, object_related: Dict, notif_type: str):
        time.sleep(10)
        app_label = object_related['app_label']
        object_name = object_related['object_name']
        id = object_related['id']

        object_related = apps.get_model(
            app_label, object_name, require_ready=True
        )._default_manager.get(pk=id)

        notif_type_fnct = {
            constants.NEW_BLOG_POST: cls().announce_new_blog,
            constants.NEW_COMMENT: cls().announce_new_comment,
            constants.NEW_VOTE: cls().announce_new_vote,
            constants.NEW_FOLLOWER: cls().announce_new_follower,
            constants.NEW_QUESTION: cls().announce_new_question,
            constants.NEW_ANSWER: cls().announce_new_answer,
            constants.ANSWER_ACCEPTED: cls().announce_answer_accepted,
        }
        return notif_type_fnct[notif_type](object_related, notif_type)

    def announce_new_follower(self, writter, notif_type):
        return[{
            "email": self.save_notif(
                writter,
                writter,
                notif_type,
                {
                    "subject": constants.NEW_FOLLOWER,
                    "content": (
                        "Tus blogs sigen pagando, tu comunidad de lectores sigue aumentando día a día, felicitaciones"
                    ),
                }
            ),
            "receiver_id": writter.id,
            "is_for": constants.EMAIL_FOR_NOTIFICATION
        }]

    def announce_new_comment(self, obj, notif_type):
        return[{
            "email": self.save_notif(
                obj,
                obj.author,
                notif_type,
                {
                    "subject": constants.NEW_COMMENT,
                    "content": f"{obj.title} ha recibido un nuevo comentario",
                }
            ),
            "receiver_id": obj.author.id,
            "is_for": constants.EMAIL_FOR_NOTIFICATION
        }]

    def announce_new_vote(self, obj, notif_type):
        return[{
            "email": self.save_notif(
                obj,
                obj.author,
                notif_type,
                {
                    "subject": constants.NEW_VOTE,
                    "content": f"{obj.title} ha recibido un nuevo voto",
                }
            ),
            "receiver_id": obj.author.id,
            "is_for": constants.EMAIL_FOR_NOTIFICATION
        }]

    def announce_new_question(self, question, notif_type):
        notif_info = []
        for user in User.objects.all().exclude(pk=question.author.pk):
            title = question.title[:15]
            subject = f"{constants.NEW_QUESTION} {title}..."
            email = self.save_notif(
                question,
                user,
                notif_type,
                {
                    "subject": subject,
                    "content": question.content,
                }
            )
            notif_info.append(
                {
                    "email": email,
                    "receiver_id": user.id,
                    "is_for": constants.EMAIL_FOR_NOTIFICATION
                }
            )
        return notif_info

    def announce_new_blog(self, blog, notif_type):
        # blog.author.main_writter_followed.followers.all() that should be the actual loop over, all the writter's followers
        notif_info = []
        for user in User.objects.all().exclude(pk=blog.author.pk):
            email = self.save_notif(
                blog,
                user,
                notif_type,
                {
                    "subject": blog.title,
                    "content": blog.resume,
                }
            )
            notif_info.append(
                {
                    "email": email,
                    "receiver_id": user.id,
                    "is_for": constants.EMAIL_FOR_NOTIFICATION
                }
            )
        return notif_info

    def announce_new_answer(self, answer, notif_type):
        notif_info = []
        question = answer.question_related
        for user in question.related_users:
            title = question.title[:15]
            subject = f"{title}... tiene una nueva respuesta"
            if question.author == user:
                subject = "Tu pregunta tiene una nueva respuesta"
            email = self.save_notif(
                answer,
                user,
                notif_type,
                {
                    "subject": subject,
                    "content": answer.content,
                }
            )
            notif_info.append(
                {
                    "email": email,
                    "receiver_id": user.id,
                    "is_for": constants.EMAIL_FOR_NOTIFICATION
                }
            )
        return notif_info

    def announce_answer_accepted(self, answer, notif_type):
        notif_info = []
        question = answer.question_related
        for user in question.related_users:
            title = question.title[:15]
            subject = f"{title}... tiene una respuesta acceptada"
            if question.has_accepted_answer and question.accepted_answer.author == user:
                subject = "Tu respuesta ha sido acceptada"
            email = self.save_notif(
                answer,
                user,
                notif_type,
                {
                    "subject": subject,
                    "content": answer.content,
                }
            )
            notif_info.append(
                {
                    "email": email,
                    "receiver_id": user.id,
                    "is_for": constants.EMAIL_FOR_NOTIFICATION
                }
            )
        return notif_info
