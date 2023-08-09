from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.sessions.models import Session

from geoip2.errors import AddressNotFoundError

from src.seo.models import Visiteur


class SeoInformation:
    @staticmethod
    def get_client_ip(request) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        elif request.META.get("HTTP_X_REAL_IP"):
            ip = request.META.get("HTTP_X_REAL_IP")
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def add_visiteur_id_into_session(request, visiteur: Visiteur) -> None:
        request.session["visiteur_id"] = visiteur.id
        request.session.modified = True
        request.session.save()

    def meta_information(self, request) -> Dict[str, Any]:
        ip = self.get_client_ip(request)
        if settings.DEBUG:
            ip = "162.158.50.77"

        meta_information = {"http_user_agent": request.META.get("HTTP_USER_AGENT"), "ip": ip}
        try:
            location_info = GeoIP2().city(ip)
            meta_information.update(location_info)
        except AddressNotFoundError:
            pass
        return meta_information

    def update_visiteur_session(self, visiteur: Visiteur, request) -> Visiteur:
        if not request.session or not request.session.session_key:
            request.session.save()
        visiteur.session_id = request.session.session_key
        visiteur.save(update_fields=["session_id"])
        self.add_visiteur_id_into_session(request, visiteur)
        return visiteur

    def get_visiteur_by_old_session(self, request) -> Optional[Visiteur]:
        session = Session.objects.filter(session_key=request.session.session_key)
        if session.exists():
            session_obj = Session.objects.get(session_key=request.session.session_key)
            session_obj_visiteur_id = session_obj.get_decoded().get("visiteur_id")
            if session_obj_visiteur_id:
                return Visiteur.objects.get(id=session_obj_visiteur_id)
        return None

    def create_visiteur(self, request) -> Visiteur:
        meta_visiteur = self.meta_information(request)
        if not request.session or not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        visiteur = Visiteur.objects.create(session_id=session_id, **meta_visiteur)
        self.add_visiteur_id_into_session(request, visiteur)
        return visiteur

    def find_visiteur(self, request) -> Visiteur:
        # TODO break it into smaller pieces
        seo = self.meta_information(request)
        visiteur = self.get_visiteur_by_old_session(request)
        if not visiteur:
            find_visiteur = Visiteur.objects.filter(ip=seo["ip"])
            if find_visiteur.exists():
                if find_visiteur.count() != 1:
                    second_filter = find_visiteur.filter(
                        http_user_agent=seo["http_user_agent"]
                    )
                    if second_filter.exists():
                        if second_filter.count() != 1:
                            visiteur = self.create_visiteur(request)
                        else:
                            visiteur = Visiteur.objects.get(
                                ip=seo["ip"], http_user_agent=seo["http_user_agent"]
                            )
                            self.update_visiteur_session(visiteur, request)
                    else:
                        visiteur = self.create_visiteur(request)
                else:
                    visiteur = Visiteur.objects.get(ip=seo["ip"])
                    self.update_visiteur_session(visiteur, request)
            else:
                visiteur = self.create_visiteur(request)
        return visiteur
