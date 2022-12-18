from django.views.generic import RedirectView
from django.contrib import messages

from src.seo.views import SEOListView, SEOCreateView, SEOTemplateView
from .outils.socialposter.facepy import Facebook
from .models import SocialmediaAuth


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
            facebook_response_code = self.request.GET["code"]
            facebook_response_state = self.request.GET["state"]
            messages.success(self.request, f"No error")
        except KeyError:
            messages.error(self.request, f"Error")

    def get(self, request, *args, **kwargs):
        self.get_facebook_params_response()
        return super().get(request, *args, **kwargs)
    