from django.contrib import messages
from django.views.generic import RedirectView

from src.seo.views import SEOCreateView, SEOListView, SEOTemplateView

from .models import SocialmediaAuth
from .outils.socialposter.facepy import Facebook


class ManageAddSocialmediasTempalteView(SEOTemplateView):
    template_name = "modals/add-socialmedia.html"
    private_view = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["facebook_auth"] = Facebook.authorisation_url()
        return context


class ManageSocialmediasView(SEOListView):
    template_name = "manage-socialmedias.html"
    meta_title = "Maneja tus redes sociales"
    private_view = True
    model = SocialmediaAuth

    def get_queryset(self):
        return SocialmediaAuth.objects.get_user_socialmedias(self.request.user)


class ManageSocialmediaCreateView(SEOCreateView):
    template_name = "add-socialmedia.html"
    model = SocialmediaAuth
    private_view = True


class FacebookAuthRedirectView(RedirectView):
    permanent = True
    pattern_name = "users:user-detail-view"

    def get_facebook_params_response(self):
        try:
            self.request.GET["code"]
            self.request.GET["state"]
            messages.success(self.request, "No error")
        except KeyError:
            messages.error(self.request, "Error")

    def get(self, request, *args, **kwargs):
        self.get_facebook_params_response()
        return super().get(request, *args, **kwargs)
