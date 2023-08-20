from src.escritos.api.abstract import AbstractWrittenContentSerializer

from ..models import PublicBlog


class SimpleBlogSerializer(AbstractWrittenContentSerializer):
    class Meta(AbstractWrittenContentSerializer.Meta):
        model = PublicBlog
