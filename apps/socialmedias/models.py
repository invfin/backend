from ckeditor.fields import RichTextField

from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    JSONField,
    ManyToManyField,
    Model,
    PositiveIntegerField,
)

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.general.mixins import BaseToAllMixin
from apps.content_creation.models import DefaultContent, DefaultTilte, Emoji, Hashtag
from apps.content_creation.constants import POST_TYPE, SOCIAL_MEDIAS

User = get_user_model()


class AbstractContentShared(Model, BaseToAllMixin):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    date_shared = DateTimeField(auto_now_add=True)
    post_type = PositiveIntegerField(choices=POST_TYPE)
    platform_shared = CharField(max_length=500, choices=SOCIAL_MEDIAS)
    social_id = CharField(max_length=500)
    title = RichTextField(blank=True)
    content = RichTextField(blank=True)
    default_title = ForeignKey(DefaultTilte, on_delete=SET_NULL, null=True, blank=True)
    default_content = ForeignKey(DefaultContent, on_delete=SET_NULL, null=True, blank=True)
    title_emojis = ManyToManyField(Emoji, blank=True)
    hashtags = ManyToManyField(Hashtag, blank=True)
    extra_description = RichTextField(blank=True)
    metadata = JSONField(default=dict)

    class Meta:
        abstract = True


class TermSharedHistorial(AbstractContentShared):
    content_shared = ForeignKey(Term, on_delete=CASCADE, null=True, blank=True, related_name="terms_shared")

    class Meta:
        verbose_name = "Term shared"
        db_table = "shared_terms"


class QuestionSharedHistorial(AbstractContentShared):
    content_shared = ForeignKey(Question, on_delete=CASCADE, null=True, blank=True, related_name="questions_shared")

    class Meta:
        verbose_name = "Question shared"
        db_table = "shared_questions"


class BlogSharedHistorial(AbstractContentShared):
    content_shared = ForeignKey(PublicBlog, on_delete=CASCADE, null=True, blank=True, related_name="blogs_shared")

    class Meta:
        verbose_name = "Blog shared"
        db_table = "shared_blogs"


class ProfileSharedHistorial(AbstractContentShared):
    content_shared = ForeignKey(
        WritterProfile, on_delete=CASCADE, null=True, blank=True, related_name="profiles_shared"
    )

    class Meta:
        verbose_name = "Profile shared"
        db_table = "shared_profiles"


class CompanySharedHistorial(AbstractContentShared):
    content_shared = ForeignKey(Company, on_delete=CASCADE, null=True, blank=True, related_name="company_shared")

    class Meta:
        verbose_name = "Company shared"
        db_table = "shared_companies"


class NewsSharedHistorial(AbstractContentShared):
    company_related = ForeignKey(Company, on_delete=CASCADE, null=True, blank=True, related_name="news_shared")

    class Meta:
        verbose_name = "Company news shared"
        db_table = "shared_news"
