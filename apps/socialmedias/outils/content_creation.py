from typing import Dict, List, Any
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants


class ContentCreation:
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
        """
        default_title_position may be Beginning, End
        emoji_x_position may be Beginning, Middle, End
        """
        title_dict = dict()
        base_title = "_beginning_emoji__beginning_default_title__middle_b_emoji__actual_title__middle_e_emoji__ending_default_title__ending_emoji_"
        if customize_title:
            default_title_filter = custom_title_info.get("default_title_filter", {})
            default_title = DefaultTilte.objects.random_title(default_title_filter)
            title_dict["default_title"] = default_title
            if not title:
                pre_final_title = f"_beginning_emoji_{default_title.title}_ending_emoji_"
            else:
                pre_final_title = base_title.replace("_actual_title_", title)
                if custom_title_info["default_title_position"] == "Beginning":
                    pre_final_title = pre_final_title.replace(
                        "_beginning_default_title_", default_title.title
                    )
                    emoji_place_rm = "_middle_e_emoji_"
                    emoji_place_change = "_middle_b_emoji_"
                else:
                    pre_final_title = pre_final_title.replace(
                        "_ending_default_title_", default_title.title
                    )
                    emoji_place_rm = "_middle_b_emoji_"
                    emoji_place_change = "_middle_e_emoji_"
                pre_final_title = pre_final_title.replace(emoji_place_change, "_middle_emoji_")
                pre_final_title = pre_final_title.replace(emoji_place_rm, "")
        else:
            if title:
                pre_final_title = f"_beginning_emoji_{title}_ending_emoji_"
            else:
                raise Exception("A title needs to be set")
        if use_emojis:
            emojis = Emoji.objects.random_emojis(len(emojis_info.keys()))
            title_dict["emojis"] = emojis
            for index, emoji in enumerate(emojis):
                emoji = emoji.emoji
                if emojis_info[f"emoji_{index}_position"] == "Beginning":
                    pre_final_title = pre_final_title.replace("_beginning_emoji_", emoji)
                elif emojis_info[f"emoji_{index}_position"] == "End":
                    pre_final_title = pre_final_title.replace("_ending_emoji_", emoji)
                elif emojis_info[f"emoji_{index}_position"] == "Middle":
                    if "_middle_emoji_" in pre_final_title:
                        pre_final_title = pre_final_title.replace("_middle_emoji_", emoji)

        for parameter in ["_beginning_emoji_", "_ending_emoji_", "_middle_emoji_"]:
            if parameter in pre_final_title:
                pre_final_title = pre_final_title.repalce(parameter, "")

        title_dict["title"] = pre_final_title
        return title_dict

    @classmethod
    def create_content(cls, content: str = "", filter: Dict = {}) -> Dict:
        content_dict = {"content": content}
        if not content:
            content = DefaultContent.objects.random_content(filter)
            content_dict["default_content"] = content
            content_dict["content"] = content.content
        return content_dict
