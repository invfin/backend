from typing import Dict, Tuple
from apps.web.models import WebsiteEmail, WebsiteEmailsType
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants


class ContentCreation:
    @classmethod
    def create_title(cls, title: str = None, filter: Dict = {}) -> Dict:
        title_dict = {"title": title}
        if not title:
            title = DefaultTilte.objects.random_title(filter)
            title_dict["default_title"] = title
            title_dict["title"] = title.title
        return title_dict

    @classmethod
    def create_content(cls, content: str = None, filter: Dict = {}) -> Dict:
        content_dict = {"content": content}
        if not content:
            content = DefaultContent.objects.random_content(filter)
            content_dict["default_content"] = content
            content_dict["content"] = content.content
        return content_dict

    @classmethod
    def create_emojis(cls) -> Tuple[Emoji, Emoji]:
        emojis = Emoji.objects.random_emojis(2)
        first_emoji = emojis[0]
        last_emoji = emojis[1]
        return first_emoji, last_emoji

    @classmethod
    def create_save_email(
        cls,
        web_email_type: str,
        title: str = None,
        content: str = None,
        title_filter: Dict = {},
        content_filter: Dict = {},
    ) -> WebsiteEmail:
        base_filters = {"for_content": social_constants.WEB, "purpose": web_email_type}
        title_filter.update(base_filters)
        content_filter.update(base_filters)

        title_dict = cls.create_title(title, title_filter)
        content_dict = cls.create_content(content, content_filter)
        first_emoji, last_emoji = cls.create_emojis()

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
