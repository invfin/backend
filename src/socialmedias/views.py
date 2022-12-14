from django.views.generic import RedirectView
from django.contrib import messages

from src.socialmedias.outils.socialposter.facepy import Facebook


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
    