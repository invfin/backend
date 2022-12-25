from django.test import TestCase

from bfet import DjangoTestingModel

from src.escritos.models import Term
from src.classifications.models import Tag


class TestAbstractWrittenContent(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = DjangoTestingModel.create(Tag, name="onemore", slug="onemore")

    def test_add_tags(self):
        term = DjangoTestingModel.create(Term)
        term.add_tags(["this tag", "", "OneMore"])
        assert term.tags.filter(id=self.tag.id).exists() is True
        assert 2 == term.tags.count()
