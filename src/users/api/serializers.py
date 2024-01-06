from django.conf import settings
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from src.users.models import User

FULL_DOMAIN = settings.FULL_DOMAIN


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


class GetUserSerializer(serializers.ModelSerializer):
    # TODO: create a facade for the model user/profile/writer_profile
    # the idea would be to use this interface instead of the models
    # we can serialize data for get requests using loops from model.__dict__.pop(field)
    credits = serializers.SerializerMethodField(read_only=True)
    reputation = serializers.SerializerMethodField(read_only=True)
    has_favs_companies = serializers.SerializerMethodField(read_only=True)
    has_portfolio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        snake_to_camel = True
        model = User
        fields = [
            "username",
            "email",
            "credits",
            "reputation",
            "foto",
            "is_writer",
            "is_staff",
            "has_favs_companies",
            "has_portfolio",
            "has_investor_profile",
        ]

    @staticmethod
    def snake_to_camel(snake_str: str):
        idx = snake_str.find("_")
        while idx != -1:
            snake_str = snake_str[:idx] + snake_str[idx + 1].upper() + snake_str[idx + 2 :]
            idx = snake_str.find("_")
        return snake_str

    @property
    def data(self):
        ret = super().data
        if self.Meta.snake_to_camel:
            for key in list(ret.keys()):
                ret[self.snake_to_camel(key)] = ret.pop(key)
        return ReturnDict(ret, serializer=self)

    def get_credits(self, obj: User):
        return obj.user_profile.creditos

    def get_reputation(self, obj: User):
        return obj.user_profile.reputation_score

    def get_has_favs_companies(self, obj: User):
        return obj.favorites_companies.stock.all().exists()

    def get_has_portfolio(self, obj: User):
        return bool(obj.net_worth)


class CreateUserSerializer(serializers.ModelSerializer):
    # TODO: finish that
    class Meta:
        model = User
        fields = ["username", "first_name", "url"]


class UpdateUserSerializer(serializers.ModelSerializer):
    # TODO: finish that
    class Meta:
        model = User
        fields = ["username", "first_name", "url"]
