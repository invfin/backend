from unittest import skip
from unittest.mock import patch

from bfet import DjangoTestingModel

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from src.seo.models import Visiteur
from src.seo.outils.visiteur_meta import SeoInformation


class TestSeoInformation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().request()
        cls.request.META = {
            "HTTP_X_FORWARDED_FOR": "203.0.113.195, 70.41.3.18, 150.172.238.178",
            "HTTP_X_REAL_IP": "162.158.50.77",
            "REMOTE_ADDR": "198.456.53.65",
        }
        cls.expected_location = {
            "country_code": "ES",
            "country_name": "Spain",
            "dma_code": "",
            "is_in_european_union": "",
            "latitude": "",
            "longitude": "",
            "city": "Barcelona",
            "region": "Cataluña",
            "time_zone": "",
            "postal_code": "08015",
            "continent_code": "EU",
            "continent_name": "Europe",
        }
        cls.middleware = SessionMiddleware()
        cls.visiteur = Visiteur.objects.create()

    def setUp(self) -> None:
        self.request.session = self.client.session

    def test_get_client_ip(self):
        forwarded = SeoInformation.get_client_ip(self.request)
        assert "150.172.238.178" == forwarded

        self.request.META.pop("HTTP_X_FORWARDED_FOR")
        real_ip = SeoInformation.get_client_ip(self.request)
        assert "162.158.50.77" == real_ip

        self.request.META.pop("HTTP_X_REAL_IP")
        remote_addr = SeoInformation.get_client_ip(self.request)
        assert "198.456.53.65" == remote_addr

    def test_add_visiteur_id_into_session(self):
        assert self.request.session.get("visiteur_id") is None
        SeoInformation.add_visiteur_id_into_session(self.request, self.visiteur)
        assert self.request.session["visiteur_id"] == self.visiteur.id

    @patch("django.contrib.gis.geoip2.base.GeoIP2.city")
    def test_meta_information(self, mock_city):
        mock_city.return_value = self.expected_location
        meta_information = SeoInformation().meta_information(self.request)
        expected_result = {
            "http_user_agent": None,
            "ip": "150.172.238.178",
            **self.expected_location,
        }
        assert expected_result == meta_information

    def test_update_visiteur_session(self):
        visiteur = SeoInformation().update_visiteur_session(self.visiteur, self.request)
        session = self.client.session
        assert session["visiteur_id"] == visiteur.id
        assert session.session_key == visiteur.session_id

    def test_get_visiteur_by_old_session(self):
        not_found_visiteur = SeoInformation().get_visiteur_by_old_session(self.request)
        assert not_found_visiteur is None
        visiteur = DjangoTestingModel.create(Visiteur)
        self.request.session["visiteur_id"] = visiteur.id
        self.request.session.save()
        found_visiteur = SeoInformation().get_visiteur_by_old_session(self.request)
        assert visiteur == found_visiteur

    @patch("django.contrib.gis.geoip2.base.GeoIP2.city")
    def test_create_visiteur(self, mock_city):
        assert 1 == Visiteur.objects.all().count()
        mock_city.return_value = self.expected_location
        visiteur = SeoInformation().create_visiteur(self.request)
        assert 2 == Visiteur.objects.all().count()
        assert "150.172.238.178" == visiteur.ip
        assert self.request.session.session_key == visiteur.session_id
        assert "ES" == visiteur.country_code
        assert "Spain" == visiteur.country_name
        assert "" == visiteur.dma_code
        assert "" == visiteur.is_in_european_union
        assert "" == visiteur.latitude
        assert "" == visiteur.longitude
        assert "Barcelona" == visiteur.city
        assert "Cataluña" == visiteur.region
        assert "" == visiteur.time_zone
        assert "08015" == visiteur.postal_code
        assert "EU" == visiteur.continent_code
        assert "Europe" == visiteur.continent_name
        assert None == visiteur.http_user_agent

    @patch("django.contrib.gis.geoip2.base.GeoIP2.city")
    def test_find_visiteur(self, mock_city):
        with self.subTest("Visiteur found"):
            assert 1 == Visiteur.objects.all().count()
            self.request.session["visiteur_id"] = self.visiteur.id
            self.request.session.save()
            visiteur_found = SeoInformation().find_visiteur(self.request)
            assert visiteur_found == self.visiteur
            assert 1 == Visiteur.objects.all().count()
        with self.subTest("Visiteur created"):
            self.request.session.pop("visiteur_id")
            self.request.session.save()
            mock_city.return_value = self.expected_location
            visiteur_found = SeoInformation().find_visiteur(self.request)
            assert "150.172.238.178" == visiteur_found.ip
            assert self.request.session.session_key == visiteur_found.session_id
            assert "ES" == visiteur_found.country_code
            assert "Spain" == visiteur_found.country_name
            assert "" == visiteur_found.dma_code
            assert "" == visiteur_found.is_in_european_union
            assert "" == visiteur_found.latitude
            assert "" == visiteur_found.longitude
            assert "Barcelona" == visiteur_found.city
            assert "Cataluña" == visiteur_found.region
            assert "" == visiteur_found.time_zone
            assert "08015" == visiteur_found.postal_code
            assert "EU" == visiteur_found.continent_code
            assert "Europe" == visiteur_found.continent_name
            assert None == visiteur_found.http_user_agent
            assert 2 == Visiteur.objects.all().count()
