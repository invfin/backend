from django.contrib.auth import get_user_model

from apps.seo.models import Visiteur
from apps.web.outils.content_creation import ContentCreation
from apps.web.models import WebsiteEmailTrack
from apps.web.utils import more_than_month
from apps.web import constants

User = get_user_model()


class EngagementMachine:
    def periodic_engagement(self):
        for user in User.objects.all():
            pass

    def prepare_engagement_by_user(self, user: User):
        pass

    def prepare_engagement_by_visiteur(self, visiteur: Visiteur):
        pass

    def send_website_email_engagement(self, user: User):
        last_email_engagement = WebsiteEmailTrack.objects.filter(
            sent_to=user,
            email_related__sent=True,
            email_related__type_related__slug__startswith=constants.CONTENT_FOR_ENGAGEMENT,
        )
        if last_email_engagement.exists():
            # If an email for engagement has already been sent
            if last_email_engagement.opened is True:
                pass
            else:
                pass
            # we check when was the last time the user visited the web
            if (
                user.last_time_seen
                and more_than_month(user.last_time_seen, last_email_engagement.date_to_send)
                # If the user hasn't visited the web in the last month (29 days)
            ):
                web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_LITTLE_ACTIVE
            elif (
                not user.last_time_seen
                and more_than_month(last_email_engagement.date_to_send)
                # If the user has never visited the web and the last email was sent more then a month back
            ):
                web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_NO_ACTIVE
        else:
            web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_FIRST_CALL

        return ContentCreation.create_save_email(web_objective)
