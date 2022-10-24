from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from apps.seo.outils.visiteur_meta import SeoInformation


def get_visiteur(request):
    """
    Creates a new attribute, _cached_visiteur to the request object,
    same as the user but for visitor
    """
    if not hasattr(request, "_cached_visiteur"):
        request._cached_visiteur = SeoInformation().find_visiteur(request)
    return request._cached_visiteur


class VisiteurMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``visiteur`` attribute to the current request.
    TODO: If the request comes from an API endpoint the user won't have the is_authenticated
    """
    def process_request(self, request):
        """
        Adds a ``visiteur`` attribute to the ``request`` parameter.
        """
        if not hasattr(request, "is_visiteur"):
            if request.user.is_authenticated:
                request.visiteur = None
                request.is_visiteur = False
            else:
                request.is_visiteur = True
                request.visiteur = SimpleLazyObject(lambda: get_visiteur(request))
