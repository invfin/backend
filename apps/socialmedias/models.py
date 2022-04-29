from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    DateTimeField,
    PositiveBigIntegerField,
    BooleanField
)
from django.contrib.auth import get_user_model
from django.urls import reverse

from ckeditor.fields import RichTextField

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.empresas.models import Company

from .constants import SOCIAL_MEDIAS, POST_TYPE
from .managers import (
    HashtagsManager,
    EmojisManager,
    TitlesManager
)

User = get_user_model()


class Hashtag(Model):        
    name = RichTextField(default='')
    platform_ = CharField(max_length=500, choices=SOCIAL_MEDIAS)
    is_trending = BooleanField(default=False)
    objects = HashtagsManager()

    def __str__(self) -> str:
        return str(self.name)


class Emoji(Model):
    emoji = CharField(max_length=500)
    objects = EmojisManager()

    def __str__(self) -> str:
        return str(self.emoji)


class DefaultTilte(Model):
    title = RichTextField(default='')
    objects = TitlesManager()

    def __str__(self) -> str:
        return str(self.title)  

class BaseContentShared(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    date_shared = DateTimeField(auto_now_add=True)
    post_type = PositiveBigIntegerField(choices=POST_TYPE)
    platform_shared = CharField(max_length=500, choices=SOCIAL_MEDIAS)
    social_id = CharField(max_length=500)
    title = RichTextField(blank=True)
    description = RichTextField(blank=True)
    extra_description = RichTextField(blank=True)
    inside_information = RichTextField(blank=True)

    class Meta:
        abstract = True


class TermSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        Term,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'terms_shared')

    class Meta:
        verbose_name = "Term shared"
        db_table = "shared_terms"


class QuestionSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        Question,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'questions_shared')

    class Meta:
        verbose_name = "Question shared"
        db_table = "shared_questions"


class BlogSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        PublicBlog,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'blogs_shared')

    class Meta:
        verbose_name = "Blog shared"
        db_table = "shared_blogs"


class ProfileSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        WritterProfile,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'profiles_shared')
    
    class Meta:
        verbose_name = "Profile shared"
        db_table = "shared_profiles"


class CompanySharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        Company,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'company_shared')
    
    class Meta:
        verbose_name = "Company shared"
        db_table = "shared_companies"


class NewsSharedHistorial(BaseContentShared):
    company_related = ForeignKey(
        Company,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'news_shared')
    
    class Meta:
        verbose_name = "Company news shared"
        db_table = "shared_news"