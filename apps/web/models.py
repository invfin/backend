from ckeditor.fields import RichTextField
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    PositiveBigIntegerField,
    SlugField,
)

from apps.general.mixins import BaseToAll
from apps.general.bases import BaseEmail, BaseNewsletter
from apps.seo.models import Visiteur
from apps.socialmedias.constants import SOCIAL_MEDIAS
from apps.seo import constants
from apps.users.models import User


class WebsiteLegalPage(BaseToAll):
    title = CharField(max_length=800)
    slug = SlugField(max_length=800, null=True, blank=True)
    content = RichTextField()

    class Meta:
        ordering = ['-id']
        verbose_name = "Legal website pages"
        db_table = "website_pages_legals"
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)


class WebsiteEmailsType(BaseToAll):
    name = CharField(max_length=800)
    slug = SlugField(max_length=800, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Emails type by website"
        db_table = "website_emails_type"
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.name)
        return super().save(*args, **kwargs)


class WebsiteEmail(BaseNewsletter):
    type_related = ForeignKey(WebsiteEmailsType, null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['-id']
        verbose_name = "Emails by website"
        db_table = "website_emails"

    def __str__(self) -> str:
        return self.title
        

class WebsiteEmailTrack(BaseEmail):
    email_related = ForeignKey(
        WebsiteEmail, 
        null=True,
        blank=True,
        on_delete=SET_NULL, 
        related_name="email_related"
    )

    class Meta:
        verbose_name = "Email counting"
        db_table = "website_emails_track"
    
    def __str__(self) -> str:
        return self.email_related.title


class PromotionCampaign(BaseToAll):
    title = CharField(max_length=600, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    categories = ManyToManyField('general.Category', blank=True)
    tags = ManyToManyField('general.Tag', blank=True)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)
    email_type_related = ForeignKey(WebsiteEmailsType, null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        verbose_name = "Promotions campaigns"
        db_table = "promotions_campaigns"

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)


class Promotion(BaseToAll):
    title = CharField(max_length=600, blank=True)
    content = RichTextField()
    thumbnail = CharField(max_length=600, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    prize = PositiveBigIntegerField(default=0)
    has_prize = BooleanField(default=False)
    shareable_url = CharField(max_length=600, blank=True)
    redirect_to = CharField(max_length=600, blank=True)
    medium = CharField(max_length=250, choices=constants.MEDIUMS, blank=True)
    web_promotion_type = CharField(max_length=250, choices=constants.WEP_PROMOTION_TYPE, blank=True)
    web_location = CharField(max_length=250, choices=constants.WEP_PROMOTION_LOCATION, blank=True)
    web_place = CharField(max_length=250, choices=constants.WEP_PROMOTION_PLACE, blank=True)
    social_media = CharField(max_length=250, blank=True, choices=SOCIAL_MEDIAS)
    publication_date = DateTimeField(blank=True)
    campaign_related = ForeignKey(PromotionCampaign, on_delete=SET_NULL, null=True, blank=True)
    reuse = BooleanField(default=False)
    times_to_reuse = PositiveBigIntegerField(default=0)
    users_clicked = ManyToManyField(User, blank=True)
    visiteurs_clicked = ManyToManyField(Visiteur, blank=True)
    clicks_by_user = PositiveBigIntegerField(default=0)
    clicks_by_not_user = PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = "Promociones"
        db_table = "promotions"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)
    
    @property
    def full_url(self):
        source = 'invfin'
        if self.medium != source:            
            source = self.social_media
        utm_source = f'utm_source={source}'
        utm_medium = f'utm_medium={self.medium}'
        utm_campaign = f'utm_campaign={self.campaign_related.title}'
        utm_term = f'utm_term={self.title}'
        return f'{self.redirect_to}?{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'


class UserAndVisiteurCategory(BaseToAll):
    name = CharField(max_length=800)
    slug = SlugField(max_length=800, null=True, blank=True)
    name_for_user = CharField(max_length=800, null=True, blank=True)
    show_to_user = BooleanField(default=False)
    email_type_related = ManyToManyField(WebsiteEmailsType, blank=True)
    users = ManyToManyField(User, blank=True)
    visiteurs = ManyToManyField(Visiteur, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Category of users and visiteurs"
        db_table = "users_visiteurs_categories"
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.name)
        return super().save(*args, **kwargs)