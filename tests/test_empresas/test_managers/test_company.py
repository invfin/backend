from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import Company, Exchange, ExchangeOrganisation
from src.industries_sectors.models import Industry, Sector


class TestManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector = DjangoTestingModel.create(Sector)
        cls.industry = DjangoTestingModel.create(Industry)
        cls.exchange_org_fr = DjangoTestingModel.create(ExchangeOrganisation, name="France")
        cls.exchange_org_usa = DjangoTestingModel.create(ExchangeOrganisation, name="Estados Unidos")
        cls.exchange_nyse = DjangoTestingModel.create(Exchange, exchange_ticker="NYSE", main_org=cls.exchange_org_usa)
        cls.exchange_euro = DjangoTestingModel.create(Exchange, exchange_ticker="EURO", main_org=cls.exchange_org_fr)
        cls.apple = DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            name="apple",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=True,
            updated=False,
            has_error=True,
            exchange=cls.exchange_nyse,
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )
        cls.zinga = DjangoTestingModel.create(
            Company,
            ticker="ZNGA",
            name="zinga",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=False,
            updated=True,
            has_error=False,
            exchange=cls.exchange_nyse,
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "yes"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )
        cls.louis = DjangoTestingModel.create(
            Company,
            ticker="LVMH",
            name="louis",
            no_incs=True,
            no_bs=False,
            no_cfs=False,
            industry=cls.industry,
            description_translated=False,
            exchange=cls.exchange_euro,
            updated=False,
            has_error=False,
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )
        cls.google = DjangoTestingModel.create(
            Company,
            ticker="GOOGL",
            name="google",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=cls.sector,
            industry=cls.industry,
            description_translated=True,
            exchange=cls.exchange_nyse,
            updated=False,
            has_error=False,
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )

    def test_filter_checking(self):
        assert self.zinga in list(Company.objects.filter_checking("institutionals", True))
        companies_no_institutionals = list(Company.objects.filter_checking("institutionals", False))
        for company in [self.apple, self.google, self.louis]:
            with self.subTest(f"{company}"):
                assert company in companies_no_institutionals

    def test_companies_by_main_exchange(self):
        assert [self.apple, self.google, self.zinga] == list(
            Company.objects.companies_by_main_exchange("Estados Unidos")
        )

    def test_clean_companies(self):
        assert [self.apple, self.google, self.zinga] == list(Company.objects.clean_companies())

    def test_clean_companies_by_main_exchange(self):
        assert [self.apple, self.google, self.zinga] == list(
            Company.objects.clean_companies_by_main_exchange("Estados Unidos")
        )

    def test_complete_companies_by_main_exchange(self):
        assert [self.apple, self.google] == list(Company.objects.complete_companies_by_main_exchange("Estados Unidos"))

    def test_get_similar_companies(self):
        assert [self.apple, self.google] == list(
            Company.objects.get_similar_companies(self.sector.id, self.industry.id)
        )

    def test_clean_companies_to_update(self):
        assert [self.google] == list(Company.objects.clean_companies_to_update("Estados Unidos"))
