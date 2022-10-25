from unittest import skip

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation


class TestSeoInformation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().request()
        cls.request.META = {
            "HTTP_X_FORWARDED_FOR": "203.0.113.195, 70.41.3.18, 150.172.238.178",
            "HTTP_X_REAL_IP": "162.158.50.77",
            "REMOTE_ADDR": "198.456.53.65",
        }
        cls.middleware = SessionMiddleware()
        cls.visiteur = Visiteur.objects.create()

    def test_get_client_ip(self):
        forwarded = SeoInformation.get_client_ip(self.request)
        assert "150.172.238.178" == forwarded

        self.request.META.pop("HTTP_X_FORWARDED_FOR")
        real_ip = SeoInformation.get_client_ip(self.request)
        assert "162.158.50.77" == real_ip

        self.request.META.pop("HTTP_X_REAL_IP")
        remote_addr = SeoInformation.get_client_ip(self.request)
        assert "198.456.53.65" == remote_addr

    @skip("need GEOIP")
    def test_meta_information(self):
        meta_information = SeoInformation().meta_information(self.request)
        expected_location = {}
        expected_result = {
            "http_user_agent": "",
            "location": expected_location,
            "ip": "162.158.50.77",
        }
        assert expected_result == meta_information

    @skip("seo module fails to be imported")
    def test_update_visiteur_session(self):
        # self.middleware.process_request(self.request)
        # self.request.session.save()
        request = self.client.request()
        visiteur = SeoInformation().update_visiteur_session(self.visiteur, request)
        session = self.client.session
        assert session["visiteur_id"] == visiteur.id
        assert session.session_key == visiteur.session_id

    @skip("seo module fails to be imported")
    def test_get_visiteur_by_old_session(self):
        request = self.client.request()
        visiteur = SeoInformation().update_visiteur_session(self.visiteur, request)
        found_visiteur = SeoInformation().get_visiteur_by_old_session()
        assert visiteur == found_visiteur

        request = self.client.request()
        not_found_visiteur = SeoInformation().get_visiteur_by_old_session()
        assert not_found_visiteur is False

    @skip("seo module fails to be imported")
    def test_find_visiteur(self):
        request = self.client.request()
        visiteur_found = SeoInformation().find_visiteur(request)
        assert "" == visiteur_found.ip
        assert "" == visiteur_found.session_id
        assert "" == visiteur_found.country_code
        assert "" == visiteur_found.country_name
        assert "" == visiteur_found.dma_code
        assert "" == visiteur_found.is_in_european_union
        assert "" == visiteur_found.latitude
        assert "" == visiteur_found.longitude
        assert "" == visiteur_found.city
        assert "" == visiteur_found.region
        assert "" == visiteur_found.time_zone
        assert "" == visiteur_found.postal_code
        assert "" == visiteur_found.continent_code
        assert "" == visiteur_found.continent_name
        assert "" == visiteur_found.http_user_agent

        visiteur = SeoInformation().find_visiteur(request)
        assert "" == visiteur.ip
        assert "" == visiteur.session_id
        assert "" == visiteur.country_code
        assert "" == visiteur.country_name
        assert "" == visiteur.dma_code
        assert "" == visiteur.is_in_european_union
        assert "" == visiteur.latitude
        assert "" == visiteur.longitude
        assert "" == visiteur.city
        assert "" == visiteur.region
        assert "" == visiteur.time_zone
        assert "" == visiteur.postal_code
        assert "" == visiteur.continent_code
        assert "" == visiteur.continent_name
        assert "" == visiteur.http_user_agent

    @skip("seo module fails to be imported")
    def test_create_visiteur(self):
        request = self.client.request()
        visiteur = SeoInformation().create_visiteur(request)
        assert "" == visiteur.ip
        assert "" == visiteur.session_id
        assert "" == visiteur.country_code
        assert "" == visiteur.country_name
        assert "" == visiteur.dma_code
        assert "" == visiteur.is_in_european_union
        assert "" == visiteur.latitude
        assert "" == visiteur.longitude
        assert "" == visiteur.city
        assert "" == visiteur.region
        assert "" == visiteur.time_zone
        assert "" == visiteur.postal_code
        assert "" == visiteur.continent_code
        assert "" == visiteur.continent_name
        assert "" == visiteur.http_user_agent
