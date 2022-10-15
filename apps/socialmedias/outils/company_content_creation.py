from typing import Type, Dict

from apps.translate.google_trans_new import google_translator

from apps.empresas.models import Company
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
from apps.socialmedias.outils.content_creation import ContentCreation
from apps.socialmedias.models import NewsSharedHistorial
from apps.socialmedias import constants as socialmedias_constants


class CompanyContentCreation(ContentCreation):
    model_class = Company
    for_content = socialmedias_constants.COMPANY
    """
    crear section para reports
    crear section para company itself
    crear section para videos e imgs?
    If for twitter use $ in front of the ticker
    """

    def get_object(self, object_filter) -> Type:
        return Company.objects.get_random_most_visited_clean_company(object_filter)
    
    def create_content(self) -> Dict:
        content = f"{self.object.short_introduction} {self.object.description}"
        content_dict = {"content": content}
        return content_dict
    
    def get_object_title(self) -> str:
        return f"{}"



class CompanyNewsContentCreation(CompanyContentCreation):
    shared_model_historial = NewsSharedHistorial
    for_content = socialmedias_constants.NEWS

    def get_new_object(self, object_filter):
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
        description = news["summary"]
        media = news.get("image")
        if not media:
            media = self.object.image
        description = google_translator().translate(description, lang_src="en", lang_tgt="es")
        title = google_translator().translate(title, lang_src="en", lang_tgt="es")
        return {
            "title": self.create_random_title(title=title, default_title_filter={"for_content": self.for_content}),
            "description": description,
            "link": self.object.shareable_link,
            "media": media,
            "company_related": self.object,
            "shared_model_historial": NewsSharedHistorial,
        }


