from unittest import skip

from django.test import TestCase

from apps.api.views import BaseAPIView
from apps.api.models import CompanyRequestAPI
from apps.empresas.models import Company


@skip("Need to be better")
class TestBaseAPIView(TestCase):
    def test_get_model_to_track(self):
        view = BaseAPIView()
        with self.assertRaises(NotImplementedError, match='You need to set a "model_to_track"'):
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
        BaseAPIView().get_object_searched()

    def test_save_request(self):
        BaseAPIView().save_request()

    def test_final_responses(self):
        BaseAPIView().final_responses()

    def test_find_query_value(self):
        BaseAPIView().find_query_value()

    def test_check_limitation(self):
        BaseAPIView().check_limitation()

    def test_get_object(self):
        BaseAPIView().get_object()

    def test_generate_queryset(self):
        BaseAPIView().generate_queryset()

    def test_get(self):
        BaseAPIView().get()
