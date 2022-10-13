from typing import Dict, List
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants


class ContentCreation:
    @classmethod
    def create_title(
        cls, title: str = "", customize_title: bool = True, use_emojis: bool = True, default_title_filter: Dict = {}
    ) -> Dict:
        title_dict = {"title": title}
        if customize_title:
            default_title = DefaultTilte.objects.random_title(default_title_filter)
            title_dict["default_title"] = default_title
        if use_emojis:
            title_dict["title"] = title.title
        return title_dict

    @classmethod
    def create_content(cls, content: str = "", filter: Dict = {}) -> Dict:
        content_dict = {"content": content}
        if not content:
            content = DefaultContent.objects.random_content(filter)
            content_dict["default_content"] = content
            content_dict["content"] = content.content
        return content_dict

    @classmethod
    def create_emojis(cls, number_emojis: int = 2) -> List[Emoji]:
        return Emoji.objects.random_emojis(number_emojis)
