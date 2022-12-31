import json
from typing import Dict, Tuple
import urllib

from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic import RedirectView
from django.views.generic.edit import FormMixin

from src.general.utils import HostChecker
from src.public_blog.models import WriterProfile
from src.seo.views import SEODetailView, SEOFormView, SEOListView, SEOTemplateView
from src.web.forms import ContactForm
from src.web.models import Roadmap, WebsiteLegalPage


class CaptchaFormMixin(FormMixin):
    def get_success_url(self):
        url = reverse(self.success_url)
        return f"{url}#contact-section"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["public_key"] = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
        context["post_url"] = self.success_url
        return context

    def validate_captcha(self) -> Dict:
        recaptcha_response = self.request.POST.get("g-recaptcha-response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {"secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        captcha_response = self.validate_captcha()
        if form.is_valid() and captcha_response["success"]:
            messages.success(request, "Gracias por tu mensaje, te responderemos lo antes posible.")
            form.send_email()
            return self.form_valid(form)
        else:
            messages.error(request, "Ha habido un error con el captcha")
            return self.form_invalid(form)


class HomePage(SEOTemplateView, CaptchaFormMixin):
    success_url = "web:inicio"

    def return_writer_page_data(self, user_writer: type) -> Tuple[Dict, str]:
        context = {
            "meta_description": user_writer.user_profile.bio,
            "meta_title": user_writer.full_name,
            "meta_image": user_writer.foto,
            "current_profile": user_writer,
        }
        return context, "public/profile.html"

    def return_home_page_data(self) -> Tuple[Dict, str]:
        escritores = WriterProfile.objects.all()
        context = {
            "escritor1": escritores[0],
            "escritor2": escritores[1],
            "escritor3": escritores[2],
            "legal_links": WebsiteLegalPage.objects.all(),
        }
        return context, "home_page.html"

    def return_business_page_data(self) -> Tuple[Dict, str]:
        context = dict(
            meta_description="Ayudamos tu negocio a crecer gracias a nuestros expertos y herramientas",
            meta_tags="coach, ayuda, consultoría, software, IA, contabilidad",
            meta_title="Ayudamos tu negocio a crecer",
        )
        return context, "business_page.html"

    def get_form(self):
        return ContactForm(email_source="business-template", **self.get_form_kwargs())

    def return_page_data(self) -> Tuple[Dict, str]:
        host_checker = HostChecker(self.request)
        user_writer = host_checker.return_user_writer()
        if user_writer:
            return self.return_writer_page_data(user_writer)
        elif host_checker.host_is_business():
            return self.return_business_page_data()
        return self.return_home_page_data()

    def render_to_response(self, context, **response_kwargs):
        custom_content, template_name = self.return_page_data()
        context.update(custom_content)
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=[template_name],
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


class SupportFormView(SEOFormView, CaptchaFormMixin):
    form_class = ContactForm
    meta_title = "Soporte"
    template_name = "soporte.html"
    success_url = "web:soporte"

    def get_initial(self):
        if self.request.user.is_authenticated:
            self.initial["name"] = self.request.user.username
            self.initial["email"] = self.request.user.email
        return self.initial.copy()


class RoadmapListView(SEOListView):
    template_name = "roadmap/roadmap.html"
    model = Roadmap
    context_object_name = "objects"
    meta_title = "Roadmap"
    meta_description = "Conoce el desarrollo y pide lo que necesites"
    meta_tags = "finanzas, blog financiero, blog el financiera, invertir"
    custom_context_data = {"legal_links": WebsiteLegalPage.objects.all()}


class RoadmapDetailView(SEODetailView):
    template_name = "roadmap/roadmap_details.html"
    model = Roadmap
    context_object_name = "object"
    meta_description = "Conoce el desarrollo y pide lo que necesites"
    custom_context_data = {"show_author": False}


class LegalPages(SEODetailView):
    no_index: bool = True
    template_name = "legals.html"
    model = WebsiteLegalPage
    context_object_name = "object"
    slug_field = "slug"
    meta_description = "Todo lo que necesitas para ser un mejor inversor"
    meta_tags = "finanzas, blog financiero, blog el financiera, invertir"
    custom_context_data = {"legal_links": WebsiteLegalPage.objects.all()}


class ExcelRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse("business:product", kwargs={"slug": "excel-inteligente"})
