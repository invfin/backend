from typing import List, Tuple

from django.db.models import Manager
from django.template.defaultfilters import slugify


class TagManager(Manager):
    @staticmethod
    def clean_tag(tag: str) -> Tuple[str, str]:
        tag_name = tag.lower()
        return tag_name, slugify(tag_name)

    def retrieve_tag(self, tag: str):
        tag_name, tag_slug = self.clean_tag(tag)
        tag_obj, created = self.get_or_create(slug=tag_slug, defaults={"name": tag_name})
        return tag_obj

    def get_content_tags(self, tags: List[str]) -> List:
        return [self.retrieve_tag(tag) for tag in tags if tag]
