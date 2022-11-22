from unittest.mock import MagicMock, patch

from bfet import DjangoTestingModel

from django.db.models import QuerySet
from rest_framework.test import APITestCase

from rest_framework import status
from rest_framework.exceptions import ParseError

from apps.api.views import BaseAPIView
from apps.api.models import CompanyRequestAPI, Key
from apps.empresas.api.serializers import IncomeStatementSerializer, BasicCompanySerializer
from apps.empresas.models import Company, IncomeStatement
from apps.escritos.models import Term, TermContent
from apps.escritos.api.serializers import AllTermsSerializer
from apps.super_investors.models import Superinvestor, SuperinvestorHistory
from apps.users.models import User
from apps.business.models import ProductSubscriber
from apps.api.exceptions import WrongParameterException, ParameterNotSetException, QueryNotFoundException, ServerError


class MockRequest(MagicMock):
    def build_absolute_uri(self):
        return "/company-information/excel-api/income"


class TestBaseAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = DjangoTestingModel.create(User, first_name="Term", last_name="Autor")
        cls.key = DjangoTestingModel.create(
            Key,
            user=cls.user,
            in_use=True,
            removed=None,
        )
        cls.term = DjangoTestingModel.create(
            Term,
            id=1,
            title="Term title",
            slug="term-title",
            resume="Term resume",
            total_votes=4,
            total_views=100,
            times_shared=4,
            category=None,
            author=cls.user,
            in_text_image=False,
            non_thumbnail_url=None
        )
        cls.company = DjangoTestingModel.create(
            Company,
            ticker="INTC",
            name="Intel"
        )
        cls.superinvestor = DjangoTestingModel.create(Superinvestor)
        cls.request = MockRequest(auth=cls.key, user=cls.user)
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
        response = self.client.get(
            "/company-information/excel-api/income",
            {"api_key": self.key.key},
        )
        api_view = BaseAPIView()
        api_view.request = response.renderer_context["request"]
        api_view.url_parameters = ["ticker"]
        api_view.model_to_track = "Company"
        api_view.save_request(IncomeStatement.objects.all())
        assert CompanyRequestAPI.objects.all().count() == 1

    def test_final_response(self):
        """
        TODO test when status is not success
        """
        # with self.assertRaises(APIException):
        #     final_response_error = api_view.final_response(
        #         IncomeStatementSerializer(queryset, many=True),
        #     )
        #     assert final_response_error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        serializer = AllTermsSerializer(Term.objects.all(), many=True)
        final_response = BaseAPIView().final_response(serializer)
        assert serializer.data == final_response.data
        assert final_response.status_code == status.HTTP_200_OK

    def test_find_query_value(self):
        api_view = BaseAPIView()
        api_view.url_parameters = ["ticker"]
        assert api_view.find_query_value({"ticker": "INTC"}) == ("ticker", "INTC")
        with self.subTest("Errors"):
            with self.assertRaises(WrongParameterException):
                assert api_view.find_query_value({"not set": "INTC"})
            with self.assertRaises(WrongParameterException):
                assert api_view.find_query_value({"ticker": ""})
            with self.assertRaises(WrongParameterException):
                assert BaseAPIView().find_query_value({"not set": ""})
            with self.assertRaises(WrongParameterException):
                assert BaseAPIView().find_query_value({})

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

    def test_get_model_or_callable(self):
        api_view_queryset = BaseAPIView()
        api_view_queryset.queryset = (IncomeStatement.objects.all, True)
        api_view_model = BaseAPIView()
        api_view_model.model = (IncomeStatement, False)
        api_view_neither = BaseAPIView()
        api_view_neither.serializer_class = IncomeStatementSerializer
        assert api_view_queryset.get_model_or_callable() == (IncomeStatement.objects.all, True)
        assert api_view_model.get_model_or_callable() == (IncomeStatement, False)
        assert api_view_neither.get_model_or_callable() == (IncomeStatement, False)

    @patch("apps.api.views.BaseAPIView.find_query_value")
    def test_get_query_params(self, mock_find_query_value):
        view = BaseAPIView()
        response = self.client.get("/company-information/excel-api/income", {"api_key": "horror"})
        view.request = response.renderer_context["request"]
        with self.assertRaises(ParameterNotSetException):
            view.get_query_params()

        response = self.client.get(
            "/company-information/excel-api/income",
            {"api_key": "horror", "this": "is_called"},
        )
        view = BaseAPIView()
        view.request = response.renderer_context["request"]
        view.get_query_params()
        mock_find_query_value.assert_called_with({"this": "is_called"})

    @patch("apps.api.views.BaseAPIView.get_query_params")
    def test_generate_lookup(self, mock_get_query_params):
        assert BaseAPIView().generate_lookup() == {}
        mock_get_query_params.return_value = "ticker", "INTC"
        with self.subTest("fk_lookup_model"):
            api_view_fk_lookup_model = BaseAPIView()
            api_view_fk_lookup_model.fk_lookup_model = "company__ticker"
            assert api_view_fk_lookup_model.generate_lookup() == {"company__ticker": "INTC"}

        with self.subTest("url_parameters"):
            api_view_url_parameters = BaseAPIView()
            api_view_url_parameters.url_parameters = ["ticker"]
            assert api_view_url_parameters.generate_lookup() == {"ticker": "INTC"}

    @patch("apps.api.views.BaseAPIView.generate_lookup")
    @patch("apps.api.views.BaseAPIView.prepare_queryset")
    @patch("apps.api.views.BaseAPIView.check_limitation")
    def test_generate_queryset(self, mock_check_limitation, mock_prepare_queryset, mock_generate_lookup):
        queryset = IncomeStatement.objects.filter(**{"company__ticker": "INTC"})
        with self.subTest("not limited"):
            view_not_limited = BaseAPIView()
            mock_generate_lookup.return_value = {"company__ticker": "INTC"}
            mock_prepare_queryset.return_value = queryset, True
            generated_queryset, many = view_not_limited.generate_queryset()
            assert queryset == generated_queryset
            assert many is True
            mock_prepare_queryset.assert_called_with({"company__ticker": "INTC"})
            assert mock_check_limitation.called is False

        with self.subTest("limited"):
            sliced_queryset = queryset[:10]
            view_limited = BaseAPIView()
            view_limited.limited = True
            mock_generate_lookup.return_value = {"company__ticker": "INTC"}
            mock_prepare_queryset.return_value = queryset, True
            mock_check_limitation.return_value = sliced_queryset
            generated_queryset, many = view_limited.generate_queryset()
            mock_prepare_queryset.assert_called_with({"company__ticker": "INTC"})
            mock_check_limitation.assert_called_with(queryset)
            assert sliced_queryset == generated_queryset
            assert many is True
