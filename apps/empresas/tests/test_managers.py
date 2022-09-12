from django.test import TestCase

from apps.bfet import ExampleModel

from apps.empresas.outils.update import UpdateCompany
from apps.general.models import Sector, Industry

from apps.empresas.models import (
    Company,
    Exchange,
    ExchangeOrganisation,
    IncomeStatement
)


class TestCompanyManagers(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector = ExampleModel.create(
            Sector,
            sector='sector'
        )
        cls.industry = ExampleModel.create(
            Industry,
            industry='industry'
        )
        cls.fr_main = ExampleModel.create(
            ExchangeOrganisation,
            name='France'
        )
        cls.usa_main = ExampleModel.create(
            ExchangeOrganisation,
            name='Estados Unidos'
        )
        cls.nyse = ExampleModel.create(
            Exchange,
            exchange_ticker='NYSE',
            main_org=cls.usa_main
        )
        cls.euro = ExampleModel.create(
            Exchange,
            exchange_ticker='EURO',
            main_org=cls.fr_main
        )
        cls.apple = ExampleModel.create(
            Company,
            ticker='AAPL',
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=True,
            updated=False,
            has_error=True,
            exchange=cls.nyse,
            checkings={
                'has_institutionals': {
                    'state': 'no',
                    'time': ''
                }
            }
        )
        cls.google = ExampleModel.create(
            Company,
            ticker='GOOGL',
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=True,
            exchange=cls.nyse,
            updated=False,
            has_error=False,
            checkings={
                'has_institutionals': {
                    'state': 'no',
                    'time': ''
                }
            }
        )
        cls.zinga = ExampleModel.create(
            Company,
            ticker='ZNGA',
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=False,
            updated=True,
            has_error=False,
            exchange=cls.nyse,
            checkings={
                'has_institutionals': {
                    'state': 'yes',
                    'time': ''
                }
            }
        )
        cls.intel = ExampleModel.create(
            Company,
            ticker='INTC',
            no_incs=True,
            no_bs=False,
            no_cfs=False,
            industry=cls.industry,
            description_translated=False,
            exchange=cls.euro,
            updated=False,
            has_error=False,
            checkings={
                'has_institutionals': {
                    'state': 'no',
                    'time': ''
                }
            }
        )

    def test_filter_checkings(self):
        self.assertEqual(
            [self.zinga],
            list(Company.objects.filter_checkings("institutionals", True))
        )
        self.assertEqual(
            [self.apple, self.google, self.intel],
            list(Company.objects.filter_checkings("institutionals", False))
        )

    def test_companies_by_main_exchange(self):
        self.assertEqual(
            [self.apple, self.google, self.zinga],
            list(Company.objects.companies_by_main_exchange("Estados Unidos"))
        )

    def test_clean_companies(self):
        self.assertEqual(
            [self.apple, self.google, self.zinga],
            list(Company.objects.clean_companies())
        )

    def test_clean_companies_by_main_exchange(self):
        self.assertEqual(
            [self.apple, self.google, self.zinga],
            list(Company.objects.clean_companies_by_main_exchange("Estados Unidos"))
        )

    def test_complete_companies_by_main_exchange(self):
        self.assertEqual(
            [self.apple, self.google],
            list(Company.objects.complete_companies_by_main_exchange("Estados Unidos"))
        )

    def test_get_similar_companies(self):
        self.assertEqual(
            [self.apple, self.google],
            list(Company.objects.get_similar_companies(self.sector.id, self.industry.id))
        )

    def test_clean_companies_to_update(self):
        self.assertEqual(
            [self.google],
            list(Company.objects.clean_companies_to_update("Estados Unidos"))
        )

