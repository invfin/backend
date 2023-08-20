from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

FULL_DOMAIN = settings.FULL_DOMAIN

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "name",
            "slug",
            "image",
        ]

    def get_name(self, obj):
        return obj.full_name

    def get_slug(self, obj):
        return obj.custom_url

    def get_image(self, obj):
        return f"{FULL_DOMAIN}{obj.foto}"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "url"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"), username=username, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
