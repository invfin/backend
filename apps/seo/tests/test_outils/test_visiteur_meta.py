import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation


class TestSeoInformation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().request()
        cls.request.META = {
            "HTTP_X_FORWARDED_FOR": "203.0.113.195, 70.41.3.18, 150.172.238.178",
            "HTTP_X_REAL_IP": '162.158.50.77',
            "REMOTE_ADDR": '198.456.53.65',
        }
        cls.middleware = SessionMiddleware()
        cls.visiteur = Visiteur.objects.create()

    def test_get_client_ip(self):
        forwarded = SeoInformation.get_client_ip(self.request)
        self.assertEqual("150.172.238.178", forwarded)

        self.request.META.pop("HTTP_X_FORWARDED_FOR")
        real_ip = SeoInformation.get_client_ip(self.request)
        self.assertEqual("162.158.50.77", real_ip)

        self.request.META.pop("HTTP_X_REAL_IP")
        remote_addr = SeoInformation.get_client_ip(self.request)
        self.assertEqual("198.456.53.65", remote_addr)

    def test_meta_information(self):
        meta_information = SeoInformation().meta_information(self.request)
        expected_location = {}
        expected_result = {
            "http_user_agent": "",
            "location": expected_location,
            "ip": '162.158.50.77',
        }
        self.assertEqual(expected_result, meta_information)

    def test_update_visiteur_session(self):
        # self.middleware.process_request(self.request)
        # self.request.session.save()
        request = self.client.request()
        visiteur = SeoInformation().update_visiteur_session(self.visiteur, request)
        session = self.client.session
        self.assertEqual(session["visiteur_id"], visiteur.id)
        self.assertEqual(session.session_key, visiteur.session_id)

    def test_get_visiteur_by_old_session(self):
        request = self.client.request()
        visiteur = SeoInformation().update_visiteur_session(self.visiteur, request)
        found_visiteur = SeoInformation().get_visiteur_by_old_session()
        self.assertEqual(visiteur, found_visiteur)

        request = self.client.request()
        not_found_visiteur = SeoInformation().get_visiteur_by_old_session()
        self.assertEqual(False, not_found_visiteur)

    def test_find_visiteur(self):
        request = self.client.request()
        visiteur_found = SeoInformation().find_visiteur(request)
        self.assertEqual("", visiteur_found.ip)
        self.assertEqual("", visiteur_found.session_id)
        self.assertEqual("", visiteur_found.country_code)
        self.assertEqual("", visiteur_found.country_name)
        self.assertEqual("", visiteur_found.dma_code)
        self.assertEqual("", visiteur_found.is_in_european_union)
        self.assertEqual("", visiteur_found.latitude)
        self.assertEqual("", visiteur_found.longitude)
        self.assertEqual("", visiteur_found.city)
        self.assertEqual("", visiteur_found.region)
        self.assertEqual("", visiteur_found.time_zone)
        self.assertEqual("", visiteur_found.postal_code)
        self.assertEqual("", visiteur_found.continent_code)
        self.assertEqual("", visiteur_found.continent_name)
        self.assertEqual("", visiteur_found.http_user_agent)

        visiteur = SeoInformation().find_visiteur(request)
        self.assertEqual("", visiteur.ip)
        self.assertEqual("", visiteur.session_id)
        self.assertEqual("", visiteur.country_code)
        self.assertEqual("", visiteur.country_name)
        self.assertEqual("", visiteur.dma_code)
        self.assertEqual("", visiteur.is_in_european_union)
        self.assertEqual("", visiteur.latitude)
        self.assertEqual("", visiteur.longitude)
        self.assertEqual("", visiteur.city)
        self.assertEqual("", visiteur.region)
        self.assertEqual("", visiteur.time_zone)
        self.assertEqual("", visiteur.postal_code)
        self.assertEqual("", visiteur.continent_code)
        self.assertEqual("", visiteur.continent_name)
        self.assertEqual("", visiteur.http_user_agent)

    def test_create_visiteur(self):
        request = self.client.request()
        visiteur = SeoInformation().create_visiteur(request)
        self.assertEqual("", visiteur.ip)
        self.assertEqual("", visiteur.session_id)
        self.assertEqual("", visiteur.country_code)
        self.assertEqual("", visiteur.country_name)
        self.assertEqual("", visiteur.dma_code)
        self.assertEqual("", visiteur.is_in_european_union)
        self.assertEqual("", visiteur.latitude)
        self.assertEqual("", visiteur.longitude)
        self.assertEqual("", visiteur.city)
        self.assertEqual("", visiteur.region)
        self.assertEqual("", visiteur.time_zone)
        self.assertEqual("", visiteur.postal_code)
        self.assertEqual("", visiteur.continent_code)
        self.assertEqual("", visiteur.continent_name)
        self.assertEqual("", visiteur.http_user_agent)
