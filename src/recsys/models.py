from django.contrib.auth import get_user_model
from django.db.models import SET_NULL, BooleanField, CharField, DateTimeField, ForeignKey, JSONField, Model
from django.urls import reverse

from src.business.models import ProductComplementary
from src.empresas.models import Company
from src.escritos.models import Term
from src.general.mixins import BaseToAllMixin
from src.preguntas_respuestas.models import Question
from src.promotions.models import Promotion
from src.public_blog.models import PublicBlog
from src.seo import constants
from src.seo.models import Visiteur

User = get_user_model()


class BaseModelRecommended(Model, BaseToAllMixin):
    EXPLANATION = {
        "tags": [
            {"id": 0, "points": 0},
        ],
        "categories": [
            {"id": 0, "points": 0},
        ],
    }
    place = CharField(max_length=150, choices=constants.WEP_PROMOTION_PLACE, default=constants.SIDE)
    location = CharField(max_length=150, choices=constants.WEP_PROMOTION_LOCATION, default=constants.ALL_WEB)
    style = CharField(max_length=150, choices=constants.WEP_PROMOTION_STYLE, default=constants.SOLO)
    clicked = BooleanField(default=False)
    recommendation_personalized = BooleanField(default=False)
    recommendation_explained = JSONField(default=dict)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    """
    Sobre escribir método clean o full clean. Cojer los motivos de la personalización
    o de la recomendación y guardalos en el json.
    """

    def full_clean(self, *args, **kwargs):
        return super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recsys:recommendation_clicked", kwargs={"pk": self.pk, "object_name": self.object_name})


class BaseVisiteurModelRecommended(BaseModelRecommended):
    user = ForeignKey(Visiteur, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"Visiteur - {self.user.id}"


class BaseUserModelRecommended(BaseModelRecommended):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.user.username


class VisiteurCompanyRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company recommended for visiteur"
        db_table = "recsys_companies_recommended_visiteurs"


class UserCompanyRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company recommended for user"
        db_table = "recsys_companies_recommended_users"


class VisiteurPublicBlogRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog recommended for visiteur"
        db_table = "recsys_public_blogs_recommended_visiteurs"


class UserPublicBlogRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog recommended for user"
        db_table = "recsys_public_blogs_recommended_users"


class VisiteurQuestionRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question recommended for visiteur"
        db_table = "recsys_questions_recommended_visiteurs"


class UserQuestionRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question recommended for user"
        db_table = "recsys_questions_recommended_users"


class VisiteurTermRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for visiteur"
        db_table = "recsys_terms_recommended_visiteurs"


class UserTermRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for user"
        db_table = "recsys_terms_recommended_users"


class VisiteurProductComplementaryRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(ProductComplementary, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for visiteur"
        db_table = "recsys_product_complementary_recommended_visiteurs"


class UserProductComplementaryRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(ProductComplementary, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for user"
        db_table = "recsys_product_complementary_recommended_users"


class VisiteurPromotionRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Promotion, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for visiteur"
        db_table = "recsys_promotion_recommended_visiteurs"


class UserPromotionRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Promotion, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term recommended for user"
        db_table = "recsys_promotion_recommended_users"
