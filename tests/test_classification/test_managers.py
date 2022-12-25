from django.test import TestCase

from bfet import DjangoTestingModel

from src.classifications.managers import TagManager
from src.classifications.models import Tag


class TestAbstractWrittenContent(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = DjangoTestingModel.create(Tag, name="onemore", slug="onemore")
    
    def test_clean_tag(self):
        tag_name, tag_slug = TagManager.clean_tag("this tag")
        assert "this tag" == tag_name
        assert "this-tag" == tag_slug

        tag_name, tag_slug = TagManager.clean_tag("tHiS taG")
        assert "this tag" == tag_name
        assert "this-tag" == tag_slug
    
    def test_retrieve_tag(self):
        assert 1 == Tag.objects.count()
        this_tag = Tag.objects.retrieve_tag("this tag")
        assert "this tag" == this_tag.name
        assert "this-tag" == this_tag.slug
        assert 2 == Tag.objects.count()
        onemore_tag = Tag.objects.retrieve_tag("OneMore")
        assert "onemore" == onemore_tag.name
        assert "onemore" == onemore_tag.slug
        assert 2 == Tag.objects.count()

    def test_get_content_tags(self):
        content_tags = Tag.objects.get_content_tags(["this tag", "", "OneMore"])
        assert 2 == len(content_tags)

    
    