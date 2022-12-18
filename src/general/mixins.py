from datetime import datetime
from io import BytesIO
from typing import Any, Dict
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from PIL import Image
from rest_framework.serializers import ModelSerializer

FULL_DOMAIN = settings.FULL_DOMAIN


class ResizeImageMixin:
    def resize(self, imageField: ImageField, size: tuple, format: str = "WebP"):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert("RGB")
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format=format)  # Save resize image to bytes
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
        if hasattr(self, "custom_url"):
            url = self.custom_url
        else:
            slug = self.get_absolute_url()
            url = f"{FULL_DOMAIN}{slug}"
        return url


class CheckingsMixin:
    def has_checking(self, checking: str) -> bool:
        return self.checkings[f"has_{checking}"]["state"] == "yes"

    def modify_checking(self, checking: str, has_it: bool):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        state = "yes" if has_it else "no"
        self.checkings.update({f"has_{checking}": {"state": state, "time": ts}})
        self.save(update_fields=["checkings"])


class CommentsMixin:
    @property
    def related_comments(self):
        return self.comments_related.all()

    @property
    def encoded_url_comment(self) -> str:
        comment_url = reverse("general:create_comment_view", kwargs={"url_encoded": self.encoded_url})
        return f"{FULL_DOMAIN}{comment_url}"


class VotesMixin:
    @property
    def base_encoded_url_up(self):
        return urlsafe_base64_encode(force_bytes(f"{self.base_url_to_encode}-up"))

    @property
    def encoded_url_up(self):
        comment_url = reverse("general:create_vote_view", kwargs={"url_encoded": self.base_encoded_url_up})
        return f"{FULL_DOMAIN}{comment_url}"

    @property
    def base_encoded_url_down(self):
        return urlsafe_base64_encode(force_bytes(f"{self.base_url_to_encode}-down"))

    @property
    def encoded_url_down(self):
        comment_url = reverse("general:create_vote_view", kwargs={"url_encoded": self.base_encoded_url_down})
        return f"{FULL_DOMAIN}{comment_url}"

    @classmethod
    def action_is_upvote(cls, action: str) -> bool:
        return action == "up"

    @classmethod
    def action_is_downvote(cls, action: str) -> bool:
        return action == "down"

    @classmethod
    def not_allowed_to_vote(
        cls,
        is_upvote: bool,
        is_downvote: bool,
        user_already_upvoted: bool,
        user_already_downvoted: bool,
    ) -> bool:
        return is_upvote and user_already_upvoted or is_downvote and user_already_downvoted

    def user_already_upvoted(self, user) -> bool:
        return self.upvotes.filter(pk=user.pk).exists()

    def user_already_downvoted(self, user) -> bool:
        return self.downvotes.filter(pk=user.pk).exists()

    def vote(self, user, action: str) -> int:
        user_already_upvoted = self.user_already_upvoted(user)
        user_already_downvoted = self.user_already_downvoted(user)
        is_upvote = self.action_is_upvote(action)
        is_downvote = self.action_is_downvote(action)
        vote_result = 0
        if self.not_allowed_to_vote(is_upvote, is_downvote, user_already_upvoted, user_already_downvoted):
            return vote_result
        if is_upvote:
            if user_already_downvoted:
                self.downvotes.remove(user)
                self.upvotes.add(user)
                vote_result = 2
            elif not user_already_upvoted:
                self.upvotes.add(user)
                vote_result = 1

        elif is_downvote:
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
