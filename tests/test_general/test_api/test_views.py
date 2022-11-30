from rest_framework.test import APITestCase

from bfet import DjangoTestingModel

from apps.general.api.views import BaseVoteAndCommentView
from apps.escritos.models import Term, TermsComment


class TestBaseVoteAndCommentView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        term = DjangoTestingModel.create(Term)

    def test_get_model(self):
        BaseVoteAndCommentView().get_model()

    def test_parse_url_params(self):
        response = self.client.post()
        BaseVoteAndCommentView().parse_url_params()
