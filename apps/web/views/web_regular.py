import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView

from apps.general.utils import HostChecker
from apps.public_blog.models import WritterProfile
from apps.seo.views import SEOTemplateView, SEODetailView
from apps.web.forms import ContactForm
from apps.web.models import WebsiteLegalPage


class HomePage(SEOTemplateView):
    def render_to_response(self, context, **response_kwargs):
        writter = HostChecker(self.request).return_writter()
        if writter:
            context.update(
                {
                    "meta_description": writter.user_profile.bio,
                    "meta_title": writter.full_name,
                    "meta_image": writter.foto,
                    "current_profile": writter,
                }
            )
            template_name = "public/profile.html"
        else:
            escritores = WritterProfile.objects.all()
            context["escritor1"] = escritores[0]
            context["escritor2"] = escritores[1]
            context["escritor3"] = escritores[2]
            template_name = "home_page.html"

        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=[template_name],
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


class LegalPages(SEODetailView):
    template_name = "legals.html"
    model = WebsiteLegalPage
    context_object_name = "object"
    slug_field = "slug"
    meta_description = "Todo lo que necesitas para ser un mejor inversor"
    meta_tags = "finanzas, blog financiero, blog el financiera, invertir"


def soporte_view(request):
    initial = {}
    if request.user.is_authenticated:
        initial["name"] = request.user.username
        initial["email"] = request.user.email
    form = ContactForm(initial=initial)
    public_key = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
    context = {"form": form, "public_key": public_key, "meta_title": "Soporte"}

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {"secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result["success"]:
                messages.success(request, "Gracias por tu mensaje, te responderemos lo antes posible.")
                form.send_email()
                return redirect("web:soporte")

        messages.error(request, "Ha habido un error")
        return redirect("web:soporte")

    return render(request, "soporte.html", context)


class ExcelRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse("business:product", kwargs={"slug": "excel-inteligente"})
