from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from src.notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    message = SerializerMethodField(read_only=True)
    content_path = SerializerMethodField(read_only=True)
    sender_name = SerializerMethodField(read_only=True)
    sender_image = SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "date",
            "message",
            "content_path",
            "sender_name",
            "sender_image",
        ]

    def get_message(self, obj: Notification):
        return obj.object.title

    def get_content_path(self, obj: Notification):
        return obj.get_absolute_url()

    def get_sender_name(self, obj: Notification):
        return obj.object.author.name

    def get_sender_image(self, obj: Notification):
        return obj.object.author.foto
