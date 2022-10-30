from typing import Any, Dict
import uuid
from datetime import datetime

from io import BytesIO

from PIL import Image
from bs4 import BeautifulSoup as bs
from rest_framework.serializers import ModelSerializer

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.defaultfilters import slugify


FULL_DOMAIN = settings.FULL_DOMAIN


class ResizeImageMixin:
    def resize(self, imageField: ImageField, size: tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert("RGB")
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format="WebP")  # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f"{uuid.uuid4()}.WebP"
        imageField.save(random_name, file, save=False)


class BaseToAllMixin:
    @property
    def model_to_json(self):
        class ModelSerializerInside(ModelSerializer):
            class Meta:
                model = self
                fields = "__all__"

        return ModelSerializerInside(self, many=False).data

    @property
    def app_label(self):
        return self._meta.app_label

    @property
    def object_name(self):
        return self._meta.object_name

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def build_admin_url(self, action: str, use_full_path: bool = True) -> str:
        kwargs = {"object_id": self.id} if action not in ["changelist", "add"] else {}
        path = reverse(f"admin:{self.app_label}_{self.object_name.lower()}_{action}", kwargs=kwargs)
        if use_full_path:
            return f"{FULL_DOMAIN}{path}"
        return path

    @property
    def admin_urls(self) -> Dict:
        return {
            "changelist": self.build_admin_url("changelist"),
            "add": self.build_admin_url("add"),
            "history": self.build_admin_url("history"),
            "delete": self.build_admin_url("delete"),
            "change": self.build_admin_url("change"),
        }

    @property
    def dict_for_task(self) -> Dict:
        return {
            "app_label": self.app_label,
            "object_name": self.object_name,
            "id": self.pk,
        }

    @property
    def base_url_to_encode(self) -> str:
        return f"{self.id}-{self.app_label}-{self.object_name}"

    @property
    def encoded_url(self) -> str:
        return urlsafe_base64_encode(force_bytes(self.base_url_to_encode))

    def save_unique_field(self, field, value, extra: Any = None):
        max_length = self._meta.get_field(field).max_length
        value_to_ckeck = value
        if extra:
            value_to_ckeck = f"{value}-{extra}"
        if len(value_to_ckeck) > max_length:
            value_to_ckeck = value_to_ckeck[: max_length + 1]
        if self.__class__.objects.filter(**{field: value_to_ckeck}).exists():
            if extra and type(extra) == int:
                extra += 1
            else:
                extra = 1
            return self.save_unique_field(field, value, extra)
        if field == "slug":
            value_to_ckeck = slugify(value_to_ckeck)
        return value_to_ckeck

    @property
    def shareable_link(self):
        try:
            url = self.custom_url
        except:
            slug = self.get_absolute_url()
            url = f"{FULL_DOMAIN}{slug}"
        return url

    def has_checking(self, checking: str) -> bool:
        return self.checkings[f"has_{checking}"]["state"] == "yes"

    def modify_checking(self, checking: str, has_it: bool):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        state = "yes" if has_it else "no"
        self.checkings.update({f"has_{checking}": {"state": state, "time": ts}})
        self.save(update_fields=["checkings"])


class CommonMixin(BaseToAllMixin):
    @property
    def related_comments(self):
        return self.comments_related.all()

    @property
    def encoded_url_comment(self):
        return self.encoded_url

    @property
    def encoded_url_up(self):
        return urlsafe_base64_encode(force_bytes(f"{self.base_url_to_encode}-up"))

    @property
    def encoded_url_down(self):
        return urlsafe_base64_encode(force_bytes(f"{self.base_url_to_encode}-down"))

    def vote(self, user, action):
        user_already_upvoted = user in self.upvotes.all()
        user_already_downvoted = user in self.downvotes.all()
        vote_result = 0
        if action == "up" and user_already_upvoted or action == "down" and user_already_downvoted:
            return vote_result
        if action == "up":
            if user_already_downvoted:
                self.downvotes.remove(user)
                self.upvotes.add(user)
                vote_result = 2
            elif not user_already_upvoted:
                self.upvotes.add(user)
                vote_result = 1

        elif action == "down":
            if user_already_upvoted:
                self.upvotes.remove(user)
                self.downvotes.add(user)
                vote_result = -2
            elif not user_already_downvoted:
                self.downvotes.add(user)
                vote_result = -1

        self.author.update_reputation(vote_result)
        self.total_votes += vote_result
        self.save(update_fields=["total_votes"])
        return vote_result

    @property
    def schema_org(self):
        if self.object_name == "Question":
            schema_org = self.schema_org
        else:
            meta_url = f"{FULL_DOMAIN}/definicion/{self.slug}/"
            if self.object_name == "PublicBlog":
                meta_url = f"{self.author.custom_url}/p/{self.slug}/"
            schema_org = {
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{meta_url}"},
                "headline": f"{self.title}",
                "image": f"{self.non_thumbnail_url}",
                "datePublished": f"{self.published_at}",
                "author": {"@type": "Person", "name": f"{self.author.full_name}"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Inversiones & Finanzas",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico",
                    },
                },
            }
        return schema_org


class BaseEscritosMixins:
    def search_image(self, content):
        soup = bs(content, "html.parser")
        images = [img for img in soup.find_all("img")]
        image = False
        if len(images) != 0:
            image = images[0]
            image = image.get("src")
        return image

    def extra_info(self, image):
        if image == False:
            self.in_text_image = False
        else:
            self.in_text_image = True
            self.non_thumbnail_url = image

    def create_meta_information(self, type_content):
        from apps.seo.models import MetaParameters, MetaParametersHistorial

        meta_url = f"{FULL_DOMAIN}/definicion/{self.slug}/"
        if type_content == "blog":
            meta_url = f"{self.author.custom_url}/p/{self.slug}/"

        meta = MetaParameters.objects.create(
            meta_title=self.title,
            meta_description=self.resume,
            meta_img=self.non_thumbnail_url,
            meta_url=meta_url,
            meta_keywords=", ".join([tag.name for tag in self.tags.all()]),
            meta_author=self.author,
            published_time=self.published_at,
            modified_time=self.updated_at,
            created_at=self.created_at,
            schema_org={
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{meta_url}"},
                "headline": f"{self.title}",
                "image": f"{self.non_thumbnail_url}",
                "datePublished": f"{self.published_at}",
                "author": {"@type": "Person", "name": f"{self.author.full_name}"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Inversiones & Finanzas",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico",
                    },
                },
            },
        )
        meta_historial = MetaParametersHistorial.objects.create(
            parameter_settings=meta,
            in_use=True,
        )

        self.meta_information = meta_historial

    def save_secondary_info(self, content_type):
        if content_type != "blog":
            for term_part in self.term_parts.all():
                image = self.search_image(term_part.content)
                if image != False:
                    break
        else:
            image = self.search_image(self.content)
        self.extra_info(image)
        self.create_meta_information(content_type)
