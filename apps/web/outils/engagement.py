from typing import Dict, Type

from apps.socialmedias.outils.content_creation import (
    QuestionContentCreation,
    CompanyNewsContentCreation,
    TermContentCreation,
    PublicBlogContentCreation,
    CompanyContentCreation,
)
from apps.web.models import WebsiteEmailTrack
from apps.web.utils import more_than_month
from apps.web import constants
from apps.web.models import WebsiteEmail, Campaign
from apps.socialmedias import constants as social_constants
from apps.users.models import User


class EngagementMachine:
    content_creators_map: Dict = {
        social_constants.QUESTION_FOR_CONTENT: QuestionContentCreation,
        social_constants.NEWS_FOR_CONTENT: CompanyNewsContentCreation,
        social_constants.TERM_FOR_CONTENT: TermContentCreation,
        social_constants.PUBLIC_BLOG_FOR_CONTENT: PublicBlogContentCreation,
        social_constants.COMPANY_FOR_CONTENT: CompanyContentCreation,
    }

    def get_creator(self, content_object: str) -> Type:
        return self.content_creators_map[content_object]

    def save_newsletter(self, **kwargs) -> WebsiteEmail:
        title_emojis = kwargs.pop("title_emojis", [])
        users_selected = kwargs.pop("users_selected", [])
        web_email_newsletter_obj = WebsiteEmail.objects.create(**kwargs)
        if title_emojis:
            web_email_newsletter_obj.title_emojis.add(*title_emojis)
        if users_selected:
            web_email_newsletter_obj.users_selected.add(*users_selected)
        return web_email_newsletter_obj

    def create_newsletter(self, web_email_type: str, content_object: str, whom_to_send: str) -> WebsiteEmail:
        content_creator = self.get_creator(content_object)
        content_creator.for_content = [social_constants.WEB]
        newsletter_content_from_object = content_creator().create_newsletter_content_from_object()
        campaign, created = Campaign.objects.get_or_create(
            slug=web_email_type, defaults={"title": constants.CONTENT_PURPOSES_MAP[web_email_type]}
        )
        link = newsletter_content_from_object.pop("link")
        newsletter_content_from_object.update(
            {
                "object": newsletter_content_from_object.pop("content_shared"),
                "campaign": campaign,
                "whom_to_send": whom_to_send,
            }
        )

        return self.save_newsletter(
            **newsletter_content_from_object,
            users_selected="",
        )

    def send_website_email_engagement(self, user: User):
        last_email_engagement = WebsiteEmailTrack.objects.filter(
            sent_to=user,
            email_related__sent=True,
            email_related__campaign__slug__startswith=constants.CONTENT_FOR_ENGAGEMENT,
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
