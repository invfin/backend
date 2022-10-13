from typing import Dict

from apps.seo.models import Visiteur
from apps.socialmedias.outils.content_creation import ContentCreation
from apps.web.models import WebsiteEmailTrack
from apps.web.utils import more_than_month
from apps.web import constants
from apps.web.models import WebsiteEmail, WebsiteEmailsType
from apps.socialmedias import constants as social_constants
from apps.users.models import User


class EngagementMachine:
    def create_save_email(
        self,
        web_email_type: str,
        title: str = "",
        content: str = "",
        title_filter: Dict = {},
        content_filter: Dict = {},
    ) -> WebsiteEmail:
        base_filters = {"for_content": social_constants.WEB, "purpose": web_email_type}
        title_filter.update(base_filters)
        content_filter.update(base_filters)

        title_dict = ContentCreation.create_title(title, title_filter)  # TODO move to the correct args
        content_dict = ContentCreation.create_content(content, content_filter)
        emojis = ContentCreation.create_emojis()
        first_emoji, last_emoji = emojis[0], emojis[1]

        title = title_dict["title"]
        title_dict["title"] = f"{first_emoji}{title}{last_emoji}"
        type_related, created = WebsiteEmailsType.objects.get_or_create(slug=web_email_type)

        web_email = WebsiteEmail.objects.create(
            type_related=type_related,
            **title_dict,
            **content_dict,
        )
        web_email.title_emojis.add(first_emoji, last_emoji)
        return web_email

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

        return self.create_save_email(web_objective)
