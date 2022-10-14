from typing import Dict, List, Type, Any

from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants


class ContentCreation:
    model_class: Type = None

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
            title_dict["emojis"] = emojis
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

    @classmethod
    def create_content(cls, content: str = "", filter: Dict = {}) -> Dict:
        content_dict = {"content": content}
        if not content:
            content = DefaultContent.objects.random_content(filter)
            content_dict["default_content"] = content
            content_dict["content"] = content.content
        return content_dict


class TermContentCreation(ContentCreation):
    pass


class CompanyContentCreation(ContentCreation):
    """
    crear la section para news
    crear section para reports
    crear section para company itsel
    crear section para videos e imgs?
    """

    pass


class QuestionContentCreation(ContentCreation):
    """
    Preparar algo del estilo:
        title: la pregunta
        description: pregunta completa si hay + "las mejores respuestas por el momento son:" self.answers_set si hay
            "han aportado las siguientes"
    """

    pass
