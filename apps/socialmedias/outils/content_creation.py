import random

from typing import Dict, List, Type, Any, Tuple

from django.apps import apps
from django.conf import settings
from django.utils.html import format_html, strip_tags

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji, Hashtag
from apps.socialmedias import constants as socialmedias_constants
from apps.socialmedias.models import (
    BlogSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.seo.utils import generate_url_with_utm

FULL_DOMAIN = settings.FULL_DOMAIN


class ContentCreation:
    model_class: Type = None
    shared_model_historial: Type = None
    for_content: int = 0

    def __init__(self, platform: str) -> None:
        self.object: Type = self.get_object()
        self.platform: str = platform

    def get_object(self) -> Type:
        """Overrite this method to return the obj of the model wanted according to the random method defined

        Returns
        -------
            Type
                Return an object of the model_class defined
        """
        return self.model_class._default_manager.get_random()

    def get_shared_model_historial(self):
        if not self.shared_model_historial:
            object_name = f"{self.model_class.__name__}SharedHistorial"
            self.shared_model_historial = apps.get_model("socialmedias", object_name, require_ready=True)
        return self.shared_model_historial

    def get_object_title(self) -> str:
        return self.object.title

    def get_object_content(self) -> str:
        return self.object.resume

    def get_object_media(self) -> Any:
        return self.object.image

    @classmethod
    def create_hashtags(cls, platform: str, need_slice: bool = False, max_slice: int = 3) -> Tuple[List[Hashtag], str]:
        """Get according to the platform (socialmedia) wanted the hashtags that might be used for the content.

        Parameters
        ----------
            platform : str
                The socialmedia in which we want to post

            need_slice : bool, optional
                Specify if we need to slice the number of hashtags that we want, by default False

            max_slice : int, optional
                The number of hashtags to return if we slice them, by default 3

        Returns
        -------
            Tuple[List[Hashtag], str]
                The list of hashtag fetched for the socialmedia and a string returning the hashtags with # ready to publish
        """
        hashtags_list = Hashtag.objects.random_hashtags(platform)
        if need_slice:
            hashtags_list = random.choices(hashtags_list, k=max_slice)

        hashtags = "#" + " #".join([hashtag.title for hashtag in hashtags_list])
        return hashtags_list, hashtags

    @classmethod
    def create_utm_url(cls, *args, **kwargs) -> str:
        return generate_url_with_utm(*args, **kwargs)

    @classmethod
    def create_title(
        cls,
        title: str = "",
        customize_title: bool = True,
        custom_title_info: Dict[str, Any] = {
            "default_title_position": "Beginning",
            "default_title_filter": {},
        },
        use_emojis: bool = True,
        emojis_info: Dict[str, Any] = {
            "emoji_1_position": "Beginning",
            "emoji_2_position": "End",
        },
    ) -> Dict:
        """Method to create titles or improve them.

        Parameters
        ----------
            title : str, optional
                The title that will be used, by default ""
            customize_title : bool, optional
                A boolean to indicate if the title has to be customized adding a
                pre o post title, by default True

            custom_title_info : _type_, optional
                If the title has to be customized here the parameters are passed.
                You should pass a dict with the position that the title has to be used and
                filters to get the right titles. default_title_position may be Beginning, End,
                by default { "default_title_position": "Beginning", "default_title_filter": {}, }

            use_emojis : bool, optional
                A boolean to indicate if emojis have to be set into the title, by default True

            emojis_info : _type_, optional
                You can specify where and how many emojis should go into the title
                emoji_x_position may be Beginning, Middle, End,
                by default { "emoji_1_position": "Beginning", "emoji_2_position": "End", }

        Returns
        -------
            Dict
                With default_title, the actual title and the emojis that might be used
        """
        title_dict = dict()
        base_title = (
            "_beginning_emoji_ _beginning_default_title_ _middle_b_emoji_ _actual_title_"
            " _middle_e_emoji_ _ending_default_title_ _ending_emoji_"
        )
        if customize_title or not title:
            default_title_filter = custom_title_info.get("default_title_filter", {})
            default_title = DefaultTilte.objects.random_title(default_title_filter)
            title_dict["default_title"] = default_title
            if not title:
                pre_final_title = f"_beginning_emoji_ {default_title.title} _ending_emoji_"
            else:
                pre_final_title = base_title.replace("_actual_title_", title)
                if custom_title_info["default_title_position"] == "Beginning":
                    pre_final_title = pre_final_title.replace("_beginning_default_title_", default_title.title)
                    emoji_place_rm = "_middle_e_emoji_"
                    emoji_place_change = "_middle_b_emoji_"
                else:
                    pre_final_title = pre_final_title.replace("_ending_default_title_", default_title.title)
                    emoji_place_rm = "_middle_b_emoji_"
                    emoji_place_change = "_middle_e_emoji_"
                pre_final_title = pre_final_title.replace(emoji_place_change, "_middle_emoji_")
                pre_final_title = pre_final_title.replace(emoji_place_rm, "")
        else:
            pre_final_title = f"_beginning_emoji_ {title} _ending_emoji_"

        if use_emojis:
            emojis = Emoji.objects.random_emojis(len(emojis_info.keys()))
            title_dict["title_emojis"] = emojis
            for index, emoji in enumerate(emojis):
                index += 1
                emoji = emoji.emoji
                if emojis_info[f"emoji_{index}_position"] == "Beginning":
                    pre_final_title = pre_final_title.replace("_beginning_emoji_", emoji)
                elif emojis_info[f"emoji_{index}_position"] == "End":
                    pre_final_title = pre_final_title.replace("_ending_emoji_", emoji)
                elif emojis_info[f"emoji_{index}_position"] == "Middle":
                    if "_middle_emoji_" in pre_final_title:
                        pre_final_title = pre_final_title.replace("_middle_emoji_", emoji)

        for parameter in [
            "_beginning_emoji_",
            "_ending_emoji_",
            "_middle_emoji_",
            "_beginning_default_title_",
            "_ending_default_title_",
        ]:
            if parameter in pre_final_title:
                pre_final_title = pre_final_title.replace(parameter, "")
                pre_final_title = pre_final_title.replace("  ", " ").strip()

        final_title = pre_final_title.replace("  ", " ").strip()
        title_dict["title"] = final_title
        return title_dict

    def create_url(self):
        return self.object.shareable_link

    @classmethod
    def create_content(cls, content: Type, filter: Dict = {}) -> Dict:
        content_dict = {"content": content}
        if not content:
            content = DefaultContent.objects.random_content(filter)
            content_dict["default_content"] = content
            content_dict["content"] = content.content
        return content_dict

    def create_social_media_content_from_object(self):
        content = self.object
        title = self.get_object_title()
        content = self.get_object_content()
        need_slice = bool(self.platform == socialmedias_constants.TWITTER)
        hashtags_list, hashtags = self.create_hashtags(self.platform, need_slice)
        return {
            "title": self.create_random_title(title=title, default_title_filter={"for_content": self.for_content}),
            "content": self.create_content(content),
            "link": self.create_url(),
            "media": self.get_object_media(),
            "content_shared": self.object,
            "shared_model_historial": self.shared_model_historial,
            "hashtags_list": hashtags_list,
            "hashtags": hashtags,
        }

    @classmethod
    def create_random_title(cls, **kwargs) -> Dict:
        number_emojis = random.randint(0, 3)
        emojis_info = {}
        use_emojis = True
        if number_emojis < 1:
            use_emojis = False
        elif number_emojis == 1:
            emojis_info = {"emoji_1_position": random.choice(["Beginning", "End"])}
        else:
            for index in range(number_emojis):
                emojis_info[f"emoji_{index}_position"] = ["Beginning", "End", "Middle"][index - 1]

        custom_title_info = {
            "default_title_position": random.choice(["Beginning", "End"]),
            "default_title_filter": kwargs.get("default_title_filter", {}),
        }
        return cls.create_title(
            kwargs.get("title", ""),
            custom_title_info=custom_title_info,
            emojis_info=emojis_info,
            use_emojis=use_emojis,
        )


class PublicBlogContentCreation(ContentCreation):
    model_class = PublicBlog
    shared_model_historial = BlogSharedHistorial
    for_content = socialmedias_constants.PUBLIC_BLOG

    def create_content(self):
        return strip_tags(format_html(self.object.resume))


class TermContentCreation(ContentCreation):
    model_class = Term
    for_content = socialmedias_constants.TERM

    def get_object(self) -> Type:
        return Term.objects.random_clean()

    def create_content(self):
        link = self.create_url()
        description = (
            f"{self.object.resume} \nSi quieres conocer más a fondo puedes leer la definición entera {link}. \nEstos"
            " son los puntos claves que encontrarás:"
        )
        for index, term_content in enumerate(self.object.term_content_parts.all()):
            description = f"""{description}
            {index}.-{term_content.title}
            """
        return description


class QuestionContentCreation(ContentCreation):
    model_class = Question
    for_content = socialmedias_constants.QUESTION
    """
    Preparar algo del estilo:
        title: la pregunta
        description: pregunta completa si hay + "las mejores respuestas por el momento son:" self.answers_set si hay
            "han aportado las siguientes"
    """

    def get_object_title(self) -> str:
        return strip_tags(format_html(self.object.title))

    def create_content(self):
        return strip_tags(format_html(self.object.content))
