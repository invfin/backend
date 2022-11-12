from unittest.mock import MagicMock, patch

from bfet import DjangoTestingModel

from django.db.models import QuerySet
from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound

from apps.api.views import BaseAPIView
from apps.api.models import CompanyRequestAPI, Key
from apps.empresas.api.serializers import IncomeStatementSerializer
from apps.empresas.models import Company, IncomeStatement
from apps.escritos.models import Term, TermContent
from apps.super_investors.models import Superinvestor, SuperinvestorHistory
from apps.users.models import User
from apps.business.models import ProductSubscriber


class TestBaseAPIView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User)
        cls.key = DjangoTestingModel.create(Key, user=cls.user)
        cls.term = DjangoTestingModel.create(Term)
        cls.company = DjangoTestingModel.create(Company, ticker="INTC")
        cls.superinvestor = DjangoTestingModel.create(Superinvestor)
        cls.request = MagicMock(auth=cls.key, user=cls.user)
        for index in range(15):
            DjangoTestingModel.create(
                TermContent,
                force_create=True,
                term_related=cls.term,
            )
            DjangoTestingModel.create(
                IncomeStatement,
                force_create=True,
                company=cls.company,
            )
            DjangoTestingModel.create(
                SuperinvestorHistory,
                force_create=True,
                superinvestor_related=cls.superinvestor,
            )

    def test_get_model_to_track(self):
        view = BaseAPIView()
        with self.assertRaises(NotImplementedError):
            view.get_model_to_track()
        view.model_to_track = "Company"
        model_to_track_str = view.get_model_to_track()
        assert CompanyRequestAPI == model_to_track_str

        view.model_to_track = Company
        model_to_track_model = view.get_model_to_track()
        assert CompanyRequestAPI == model_to_track_model

        assert model_to_track_str == model_to_track_model

        view.model_to_track = "ignore"
        model_to_track_ignore = view.get_model_to_track()
        assert model_to_track_ignore is None

    def test_get_object_searched(self):
        for query, response, name, extra in [
            (self.term, self.term, "Term", ""),
            (IncomeStatement.objects.all(), self.company, "Comapny", "ticker"),
            (SuperinvestorHistory.objects.all(), self.superinvestor, "Superinvestor", ""),
            (TermContent.objects.all(), self.term, "Term content", ""),
        ]:
            with self.subTest(name):
                api_view = BaseAPIView()
                if extra:
                    api_view.url_parameters = [extra]
                assert api_view.get_object_searched(query) == response

    @patch("apps.seo.outils.visiteur_meta.SeoInformation.get_client_ip")
    def test_save_request(self, mock_get_client_ip):
        assert CompanyRequestAPI.objects.all().count() == 0
        mock_get_client_ip.return_value = "123.23.234.3"
        api_view = BaseAPIView()
        response = self.client.get("/company-information/excel-api/income")
        request = response.wsgi_request
        request.user = self.user
        request.auth = self.key
        api_view.request = request
        api_view.url_parameters = ["ticker"]
        api_view.model_to_track = "Company"
        api_view.save_request(IncomeStatement.objects.all())
        assert CompanyRequestAPI.objects.all().count() == 1

    def test_final_response(self):
        """
        TODO test when status is not success
        """
        assert CompanyRequestAPI.objects.all().count() == 0
        api_view = BaseAPIView()
        api_view.request = self.request
        api_view.url_parameters = ["ticker"]
        api_view.model_to_track = "Company"
        queryset = IncomeStatement.objects.all()
        # with self.assertRaises(APIException):
        #     final_response_error = api_view.final_response(
        #         IncomeStatementSerializer(queryset, many=True),
        #         queryset,
        #         "/company-information/excel-api/income",
        #         "123.23.234.3",
        #     )
        #     assert final_response_error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        final_response = api_view.final_response(IncomeStatementSerializer(queryset, many=True))
        assert CompanyRequestAPI.objects.all().count() == 1
        assert final_response.status_code == status.HTTP_200_OK

    def test_find_query_value(self):
        api_view = BaseAPIView()
        api_view.url_parameters = ["ticker"]
        assert api_view.find_query_value({"ticker": "INTC"}) == ("ticker", "INTC")
        assert api_view.find_query_value({"not set": "INTC"}) == (None, None)
        assert api_view.find_query_value({"not set": ""}) == (None, None)
        assert BaseAPIView().find_query_value({}) == (None, None)
        assert BaseAPIView().find_query_value({"not set": ""}) == (None, None)

    def test_check_limitation(self):
        sub_key = DjangoTestingModel.create(
            Key, user=self.user, subscription=DjangoTestingModel.create(ProductSubscriber)
        )
        api_view = BaseAPIView()
        api_view.request = MagicMock(auth=self.key, user=self.user)
        queryset = IncomeStatement.objects.all()
        sliced_query = api_view.check_limitation(queryset)
        assert len(sliced_query) == 10
        assert isinstance(sliced_query, QuerySet)

        api_view = BaseAPIView()
        request = MagicMock(auth=None, user=None)
        request.auth = sub_key
        request.user = self.user
        api_view.request = request
        not_sliced_query = api_view.check_limitation(queryset)
        assert len(not_sliced_query) == 15
        assert isinstance(not_sliced_query, QuerySet)

    def test_get_model_or_queryset(self):
        api_view_queryset = BaseAPIView()
        api_view_queryset.queryset = (IncomeStatement.objects.all, True)
        api_view_model = BaseAPIView()
        api_view_model.model = (IncomeStatement, False)
        api_view_neither = BaseAPIView()
        api_view_neither.serializer_class = IncomeStatementSerializer
        assert api_view_queryset.get_model_or_queryset() == (IncomeStatement.objects.all, True)
        assert api_view_model.get_model_or_queryset() == (IncomeStatement, False)
        assert api_view_neither.get_model_or_queryset() == (IncomeStatement, False)

    def test_get_query_params(self):
        request = MagicMock()
        response = BaseAPIView().get_query_params()
        assert {"": ""} == response

    def test_generate_lookup(self):
        assert BaseAPIView().generate_lookup() == {}
        with self.subTest("fk_lookup_model"):
            api_view_fk_lookup_model = BaseAPIView()
            api_view_fk_lookup_model.fk_lookup_model = "company__ticker"
            with self.assertRaises(ParseError):
                api_view_fk_lookup_model.generate_lookup("ticker", "")

            assert api_view_fk_lookup_model.generate_lookup("ticker", "INTC") == {"company__ticker": "INTC"}

        with self.subTest("url_parameters"):
            api_view_url_parameters = BaseAPIView()
            api_view_url_parameters.url_parameters = "ticker"
            assert api_view_url_parameters.generate_lookup("ticker", "INTC") == {"ticker": "INTC"}

    def test_generate_queryset(self):
        api_view_queryset = BaseAPIView()
        api_view_queryset.queryset = (IncomeStatement.objects.filter, True)
        with self.assertRaises(NotFound):
            api_view_queryset.generate_queryset(
                IncomeStatement.objects.filter,
                {"company__ticker": "AAPL"},
            )

        assert (
            len(
                api_view_queryset.generate_queryset(
                    IncomeStatement.objects.filter,
                    {"company__ticker": "INTC"},
                )
            )
            == 15
        )

        api_view = BaseAPIView()
        api_view.model = (Company, False)
        with self.assertRaises(NotFound):
            api_view.generate_queryset(
                Company,
                {"ticker": "AAPL"},
            )
        assert (
            api_view.generate_queryset(
                Company,
                {"ticker": "INTC"},
            )
            == self.company
        )
