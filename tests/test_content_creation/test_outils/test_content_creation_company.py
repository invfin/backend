from unittest import skip

from bfet import DjangoTestingModel, DataCreator

from django.test import TestCase

from src.socialmedias.models import CompanySharedHistorial
from src.socialmedias import constants as socialmedias_constants
from src.content_creation.outils.content_creator import CompanyContentCreation
from src.empresas.models import (
    Company,
    IncomeStatement,
    BalanceSheet,
    CashflowStatement,
)
from tests.data.empresas.empresas_data import AAPL

from .base_content_creation_mixin import BaseTestContentCreation


class TestCompanyContentCreation(BaseTestContentCreation, TestCase):
    content_creator = CompanyContentCreation
    model_class = Company
    shared_model_historial = CompanySharedHistorial

    @classmethod
    def setUpTestData(cls) -> None:
        company = DjangoTestingModel.create(
            Company,
            **AAPL,
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            has_error=False,
            description_translated=True,
        )
        DjangoTestingModel.create(IncomeStatement, company=company)
        DjangoTestingModel.create(BalanceSheet, company=company)
        DjangoTestingModel.create(CashflowStatement, company=company)
        cls.model_class_obj = company

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

    @skip("need to patch the request to get the current data + improve the description")
    def test_create_newsletter_content_from_object(self):
        pass

    @skip("need to patch the request to get the current data + improve the description")
    def test_prepare_inital_data(self):
        pass

    @skip("need to patch the request to get the current data + improve the description")
    def test_create_social_media_content_from_object(self):
        pass
