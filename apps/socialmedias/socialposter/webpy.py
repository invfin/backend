from typing import Dict, Tuple
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail, WebsiteEmailsType
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants


class Website:
    def create_title(self, title:str=None, filter:Dict={}) -> Dict:
        title_dict = {"title": title}
        if not title:
            filter.update(
                {
                    "for_content": social_constants.WEB
                }
            )
            title = DefaultTilte.objects.random_title(filter)
            title_dict['default_title'] = title
            title_dict['title'] = title.title
        return title_dict

    def create_content(self, content:str=None, filter:Dict={}) -> Dict:
        content_dict = {"content": content}
        if not content:
            filter.update(
                {
                    "for_content": social_constants.WEB
                }
            )
            content = DefaultContent.objects.random_content(filter)
            content_dict['default_content'] = content
            content_dict['content'] = content.content
        return content_dict
    
    def create_emojis(self) -> Tuple[Emoji, Emoji]:
        emojis = Emoji.objects.random_emojis(2)
        first_emoji = emojis[0]
        last_emoji = emojis[1]
        return first_emoji, last_emoji
    
    def save_email(
        self,
        web_email_type: str,
        title: str = None, 
        content: str = None,
        title_filter: Dict = {},
        content_filter: Dict = {}
    ) -> WebsiteEmail:
        title_filter.update({"purpose": web_email_type})
        content_filter.update({"purpose": web_email_type})

        title_dict = self.create_title(title, title_filter)
        content_dict = self.create_content(content, content_filter)
        first_emoji, last_emoji = self.create_emojis()

        title = title_dict["title"]
        title_dict["title"] = f"{first_emoji}{title}{last_emoji}"

        web_email = WebsiteEmail.objects.create(
            type_related = WebsiteEmailsType.objects.get(slug=web_email_type),
            **title_dict,
            **content_dict,
        )
        web_email.title_emojis.add(*[first_emoji, last_emoji])
        return web_email