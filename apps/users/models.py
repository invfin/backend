from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    Model,
    OneToOneField,
    PositiveBigIntegerField,
    TextField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.general.mixins import BaseToAllMixin, ResizeImageMixin

from apps.users.user_extension import UserExtended
from apps.users.constants import MOVE_SOURCES, MOVEMENTS
from apps.users.managers import CreditHistorialManager, ProfileManager, UserExtraManager


class User(AbstractUser, UserExtended):
    first_name = CharField(_("Nombre"), blank=True, max_length=255)
    last_name = CharField(_("Apellidos"), blank=True, max_length=255)
    is_writter = BooleanField(default=False)
    just_newsletter = BooleanField(default=False)
    just_correction = BooleanField(default=False)
    last_time_seen = DateTimeField(blank=True, null=True)
    is_recurrent = BooleanField(default=False)
    is_customer = BooleanField(default=False)
    objects = UserExtraManager()

    class Meta:
        db_table = "users"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self):
        return reverse("users:user_public_profile", kwargs={"username": self.username})


class MetaProfileInfo(Model, BaseToAllMixin):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="meta_info")
    date = DateTimeField(auto_now_add=True)
    ip = CharField(max_length=50, null=True, blank=True)
    country_code = CharField(max_length=10000, null=True, blank=True)
    country_name = CharField(max_length=10000, null=True, blank=True)
    dma_code = CharField(max_length=10000, null=True, blank=True)
    is_in_european_union = BooleanField(default=False)
    latitude = CharField(max_length=10000, null=True, blank=True)
    longitude = CharField(max_length=10000, null=True, blank=True)
    city = CharField(max_length=10000, null=True, blank=True)
    region = CharField(max_length=10000, null=True, blank=True)
    time_zone = CharField(max_length=10000, null=True, blank=True)
    postal_code = CharField(max_length=10000, null=True, blank=True)
    continent_code = CharField(max_length=10000, null=True, blank=True)
    continent_name = CharField(max_length=10000, null=True, blank=True)
    user_agent = CharField(max_length=10000, null=True, blank=True)

    class Meta:
        verbose_name = "Meta profile info"
        db_table = "user_meta_profile_information"


class MetaProfile(Model, BaseToAllMixin):
    ip = CharField(max_length=50, null=True, blank=True)
    country_code = CharField(max_length=10000, null=True, blank=True)
    country_name = CharField(max_length=10000, null=True, blank=True)
    dma_code = CharField(max_length=10000, null=True, blank=True)
    is_in_european_union = BooleanField(default=False)
    latitude = CharField(max_length=10000, null=True, blank=True)
    longitude = CharField(max_length=10000, null=True, blank=True)
    city = CharField(max_length=10000, null=True, blank=True)
    region = CharField(max_length=10000, null=True, blank=True)
    time_zone = CharField(max_length=10000, null=True, blank=True)
    postal_code = CharField(max_length=10000, null=True, blank=True)
    continent_code = CharField(max_length=10000, null=True, blank=True)
    continent_name = CharField(max_length=10000, null=True, blank=True)
    user_agent = CharField(max_length=10000, null=True, blank=True)

    class Meta:
        verbose_name = "Meta profile info"
        db_table = "meta_profile_info"


class MetaProfileHistorial(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="meta_profile")
    date = DateTimeField(auto_now_add=True)
    meta_info = ForeignKey(MetaProfile, blank=True, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Meta profile historial"
        db_table = "meta_profile_historial"


class Profile(Model, BaseToAllMixin, ResizeImageMixin):
    user = OneToOneField(User, on_delete=CASCADE, null=True, related_name="user_profile")
    reputation_score = IntegerField(default=0)
    creditos = IntegerField(default=0)
    edad = DateField("Fecha de nacimiento (DD/MM/AAAA)", null=True, blank=True)
    pais = CountryField("País de origen", null=True, blank=True, blank_label="(select country)")
    ciudad = CharField("Ciudad de origen", max_length=150, null=True, blank=True)
    # foto_perfil = CloudinaryField("Foto de perfil", 'image', null=True, width_field='image_width', height_field='image_height', default="inversorinteligente.png")
    foto_perfil = ImageField("Foto de perfil", upload_to="avatar/", default="inversorinteligente.WebP")
    bio = TextField("Descripción", null=True, blank=True)
    recommended_by = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="invited_by")
    ref_code = CharField(max_length=1000, blank=True, unique=True)
    objects = ProfileManager()

    class Meta:
        verbose_name = "Users profile"
        db_table = "profiles"

    def __str__(self) -> str:
        return self.user.full_name

    def save(self, *args, **kwargs):
        if self.ref_code == "":
            self.ref_code = Profile.objects.create_ref_code()
        super().save(*args, **kwargs)

    def transform_photo(self, img):
        self.resize(img, (400, 400))
        self.save()


class CreditUsageHistorial(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="credits_historial")
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveBigIntegerField(null=True, blank=True)
    object = GenericForeignKey("content_type", "object_id")
    date = DateTimeField(auto_now_add=True)
    amount = IntegerField()
    initial = IntegerField()
    final = IntegerField()
    movement = IntegerField(choices=MOVEMENTS)
    move_source = CharField(max_length=100, choices=MOVE_SOURCES)
    has_enought_credits = BooleanField(default=True)
    objects = CreditHistorialManager()

    class Meta:
        verbose_name = "Users credits historial"
        db_table = "user_credits_historial"

    def __str__(self) -> str:
        return self.user.full_name

    @property
    def credits_needed(self):
        return self.final
