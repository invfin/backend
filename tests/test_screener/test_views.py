from unittest.mock import MagicMock

from django.test import TestCase
from bfet import DjangoTestingModel

from src.screener.views import CompanyLookUpView
from src.empresas.models import Company


class TestCompanyLookUpView(TestCase):
    def test_company_searched_failed(self):
        with self.assertRaises(Exception):
            view = CompanyLookUpView(
                request=MagicMock(
                    GET={"stock": "Apple [AAPL]"},
                    META="path/to/META",
                )
            )
            self.assertEqual(view.company_searched(), "path/to/META")

    def test_company_searched(self):
        DjangoTestingModel.create(Company, ticker="AAPL")
        view = CompanyLookUpView(
            request=MagicMock(
                GET={"stock": "Apple [AAPL]"},
                META="path/to/META",
            )
        )
        self.assertEqual(view.company_searched(), "AAPL/")
