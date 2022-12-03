from typing import Type, Dict

from src.translate.google_trans_new import google_translator

from src.empresas.models import Company
from src.empresas.outils.retrieve_data import RetrieveCompanyData
from src.content_creation.outils.content_creator import ContentCreation
from src.socialmedias.models import NewsSharedHistorial
from src.socialmedias import constants as socialmedias_constants
from src.content_creation import constants


class CompanyContentCreation(ContentCreation):
    model_class = Company
    for_content = [constants.COMPANY]
    """
    crear section para reports
    crear section para company itself
    crear section para videos e imgs?
    If for twitter use $ in front of the ticker
    """

    def get_object(self, object_filter: Dict = {}) -> Type:
        return self.model_class._default_manager.get_random_most_visited_clean_company(object_filter)

    def get_object_content(self, **kwargs) -> str:
        return f"{self.object.short_introduction} {self.object.description}"

    def get_object_title(self) -> str:
        if self.platform == socialmedias_constants.TWITTER:
            return f"{self.object.name} ${self.object.ticker}"
        return self.object.full_name


class CompanyNewsContentCreation(CompanyContentCreation):
    shared_model_historial = NewsSharedHistorial
    for_content = [constants.NEWS]

    def get_new_object(self, object_filter: Dict = {}):
        if object_filter and "exclude" in object_filter:
            object_filter["exclude"]["id__in"].append(self.object.id)
        else:
            object_filter = {"exclude": {"id__in": [self.object.id]}}
        self.object = self.get_object(object_filter)
        return self.create_social_media_content_from_object(object_filter)

    def create_social_media_content_from_object(self, object_filter):
        news_list = RetrieveCompanyData(self.object).get_company_news()
        if not news_list:
            return self.get_new_object(object_filter)
        news: Dict = news_list[0]
        title = news["headline"]
        content = news["summary"]
        media = news.get("image")
        if not media:
            media = self.object.image

        content = google_translator().translate(content, lang_src="en", lang_tgt="es")
        title = google_translator().translate(title, lang_src="en", lang_tgt="es")

        need_slice = bool(self.platform == socialmedias_constants.TWITTER)
        hashtags_list, hashtags = self.create_hashtags(self.platform, need_slice)
        return {
            "title": self.create_random_title(
                title=title,
                default_title_filter={"for_content": self.for_content},
            ),
            "description": content,
            "link": self.create_url(),
            "media": self.get_object_media(),
            "content_shared": self.object,
            "shared_model_historial": self.shared_model_historial,
            "hashtags_list": hashtags_list,
            "hashtags": hashtags,
        }
