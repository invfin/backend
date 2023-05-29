from typing import Dict, List, Optional, Tuple, Type

from src.content_creation import constants
from src.content_creation.outils.content_creator import ContentCreation
from src.empresas.models import Company
from src.empresas.outils.retrieve_data import RetrieveCompanyData
from src.empresas.outils.company import CompanyData
from src.socialmedias import constants as socialmedias_constants
from src.socialmedias.models import NewsSharedHistorial
from src.translate.google_trans_new import google_translator


class CompanyContentCreation(ContentCreation):
    object: Company
    model_class: Type[Company] = Company
    for_content = [constants.COMPANY]
    """
    crear section para reports
    crear section para company itself
    crear section para videos e imgs?
    If for twitter use $ in front of the ticker
    """

    def get_object(self, object_filter: Optional[Dict] = None) -> Company:
        if object_filter is None:
            object_filter = {}
        return self.model_class._default_manager.get_random_most_visited_clean_company(
            **object_filter
        )

    def get_object_content(self, **kwargs) -> str:
        return f"{self.short_introduction(self.object)} {self.object.description}"

    @staticmethod
    def short_introduction(company: Company) -> str:
        current_ratios = CompanyData(company).get_ratios_information()
        last_income_statement = current_ratios["last_income_statement"]
        currency = last_income_statement.reported_currency
        try:
            cagr = round(current_ratios["cagr"], 2)
        except TypeError:
            cagr = 0

        return (
            f"{self.object.ticker} ha tenido un crecimiento en sus ingresos del {cagr}%"
            " anualizado durante los últimos 10 años. Actualmente la empresa genera"
            f" {round(last_income_statement.revenue, 2)} {currency} con gastos elevándose a"
            f" {round(last_income_statement.cost_of_revenue, 2)} {currency}. La empresa cotiza"
            f" a {round(current_ratios['current_price'], 2)} {currency} por acción, con"
            f" {current_ratios['average_shares_out']} acciones en circulación la empresa"
            " obtiene una capitalización bursátil de"
            f" {round(current_ratios['marketcap'], 2)} {currency}"
        )

    def get_object_title(self) -> str:
        if self.platform == socialmedias_constants.TWITTER:
            return f"{self.object.name} ${self.object.ticker}"
        return self.object.full_name


class CompanyNewsContentCreation(CompanyContentCreation):
    shared_model_historial = NewsSharedHistorial
    for_content = [constants.NEWS]

    def get_new_object(self, object_filter: Optional[Dict] = None):
        if object_filter is None:
            object_filter = {}
        if object_filter and "exclude" in object_filter:
            object_filter["exclude"]["id__in"].append(self.object.id)
        else:
            object_filter = {"exclude": {"id__in": [self.object.id]}}
        self.object = self.get_object(object_filter)
        return self.create_social_media_content_from_object(object_filter)

    def create_social_media_content_from_object(self, object_filter: Optional[Dict] = None):
        object_filter = object_filter or {}
        news_list = RetrieveCompanyData(self.object).get_company_news()
        if not news_list or "error" in news_list:
            return self.get_new_object(object_filter)
        title, content, media = self.get_news_content(news_list)
        need_slice = self.platform == socialmedias_constants.TWITTER
        hashtags_list, hashtags = self.create_hashtags(self.platform, need_slice)
        return {
            "title": self.create_random_title(
                title=title,
                default_title_filter={"for_content": self.for_content},
            ),
            "description": content,
            "link": self.create_url(),
            "media": media,
            "content_shared": self.object,
            "shared_model_historial": self.shared_model_historial,
            "hashtags_list": hashtags_list,
            "hashtags": hashtags,
        }

    def get_news_content(self, news_list: List[Dict[str, str]]) -> Tuple[str, str, str]:
        news = news_list[0]
        return (
            self.translate(news.get("headline", "")),
            self.translate(news.get("summary", "")),
            news.get("image", self.object.image),
        )

    @staticmethod
    def translate(content: str) -> str:
        return google_translator().translate(content, lang_src="en", lang_tgt="es")
