import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from src.seo.views import SEOCreateView, SEODetailView, SEOListView

from .forms import CreateCorrectionForm
from .models import Term, TermContent

User = get_user_model()


class GlosarioView(SEOListView):
    model = Term
    template_name = "term_inicio.html"
    ordering = ["title"]
    context_object_name = "terms"
    paginate_by = 10
    meta_description = "Todos los términos y definiciones que necesitas conocer para invertir correctamente"
    meta_tags = "finanzas, blog financiero, blog el financiera, invertir"
    meta_title = "El diccionario que necesitas como inversor"
    path_name = "recommend_side_companies"
    recsys_title = "Empresas más visitadas"

    def get_queryset(self):
        return Term.objects.clean_terms()


class TermDetailsView(SEODetailView):
    model = Term
    template_name = "term_details.html"
    context_object_name = "object"
    slug_field = "slug"
    is_article = True
    open_graph_type = "article"
    path_name = "recommend_side_companies"
    recsys_title = "Te pueden interesar"
    update_visits = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.error(self.request, "Perdón no hemos encontrado este término")
            return redirect(reverse("escritos:glosario"))
        return super().get(request, *args, **kwargs)

    def get_object(self):
        try:
            return self.model.objects.get(**self.kwargs)
        except Exception:
            return


class TermCorrectionView(SEOCreateView):
    form_class = CreateCorrectionForm
    template_name = "correction.html"
    success_message = "Gracias por tu aporte"
    no_index = True
    no_follow = True

    def get_object(self):
        return TermContent.objects.get(id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["public_key"] = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
        object = self.get_object()
        context["object"] = object
        initial = {"title": object.title, "content": object.content, "term_content_related": object}
        context["form"] = CreateCorrectionForm(initial)
        return context

    def post(self, request, *args, **kwargs):
        form = CreateCorrectionForm(request.POST)

        if self.request.user.is_anonymous:
            recaptcha_response = self.request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {"secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result["success"]:
                user = User.objects.get_or_create_quick_user(self.request, just_correction=True)
            else:
                messages.error(self.request, "Hay un error con el captcha")
                return self.form_invalid(form)
        else:
            user = self.request.user

        if form.is_valid():
            return self.form_valid(form, user)
        return self.form_invalid(form)

    def form_valid(self, form, user):
        form.instance.reviwed_by = user
        model = form.save()
        messages.success(self.request, self.success_message)
        return redirect(model.get_absolute_url())
