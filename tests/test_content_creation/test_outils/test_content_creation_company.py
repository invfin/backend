from unittest import skip

from bfet import DjangoTestingModel, DataCreator

from django.test import TestCase

from apps.empresas.models import Company
from apps.socialmedias.models import CompanySharedHistorial
from apps.socialmedias import constants as socialmedias_constants
from apps.content_creation.outils.content_creator import CompanyContentCreation

from tests.data.empresas import COMPANY_FINAL_STATEMENTS

from .base_content_creation_test import BaseTestContentCreation


class TestCompanyContentCreation(BaseTestContentCreation, TestCase):
    content_creator = CompanyContentCreation
    model_class = Company
    shared_model_historial = CompanySharedHistorial

    @classmethod
    def setUpTestData(cls) -> None:
        cls.model_class_obj = COMPANY_FINAL_STATEMENTS

    def test_get_object_title(self):
        assert self.model_class_obj.full_name == self.content_creator().get_object_title()
        assert (
            f"{self.model_class_obj.name} ${self.model_class_obj.ticker}"
            == self.content_creator(socialmedias_constants.TWITTER).get_object_title()
        )

    @skip("need to patch the request to get the current data + improve the description")
    def test_get_object_content(self):
        assert (
            f"{self.model_class_obj.short_introduction} {self.model_class_obj.description}"
            == self.content_creator().get_object_content()
        )
