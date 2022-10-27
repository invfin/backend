from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from apps.escritos.models import Term
from apps.web.models import WebsiteEmail
from apps.web.forms import WebEmailForm, AutomaticNewsletterForm
from apps.seo.views import SEOViewMixin


class BasePrivateWebView(LoginRequiredMixin, UserPassesTestMixin, SEOViewMixin):
    no_index = True
    no_follow = True

    def test_func(self):
        return self.request.user.is_superuser


class PrivateWebListView(BasePrivateWebView, ListView):
    pass


class PrivateWebDetailView(BasePrivateWebView, DetailView):
    pass


class PrivateWebUpdateView(BasePrivateWebView, UpdateView):
    pass


class PrivateWebCreateView(BasePrivateWebView, CreateView):
    pass


class PrivateWebTemplateView(BasePrivateWebView, TemplateView):
    pass


class PrivateWebFormView(BasePrivateWebView, FormView):
    pass


class ManageWebView(PrivateWebTemplateView):
    template_name = "management/inicio.html"


class ManageEmailEngagementListView(PrivateWebListView):
    template_name = "engagement/list_emails.html"
    model = WebsiteEmail
    context_object_name = "web_emails"


class AutomaticEmailNewsletterView(PrivateWebFormView):
    success_message = "Guardado correctamente"
    template_name = "modals/auto_newsletter.html"
    form_class = AutomaticNewsletterForm

    def successful_return(self):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshNewsletterList"})

    def form_valid(self, form):
        form.create_newsletter()
        return self.successful_return()


class ManageEmailEngagementUpdateView(PrivateWebUpdateView):
    model = WebsiteEmail
    form_class = WebEmailForm
    template_name = "engagement/form_email.html"
    pk_url_kwarg = "pk"

    def successful_return(self):
        messages.success(self.request, "Guardado correctamente")
        return HttpResponse(status=204, headers={"HX-Trigger": "showMessageSuccess"})

    def get_success_url(self) -> str:
        return reverse("web:manage_web")

    def form_valid(self, form) -> HttpResponse:
        seguir = dict(form.data).pop("seguir", None)
        # content not being saved
        print(form.save())
        if seguir:
            return self.successful_return()
        return HttpResponseRedirect(self.get_success_url())


class ManageEmailEngagementCreateView(PrivateWebCreateView):
    form_class = WebEmailForm
    template_name = "engagement/form_email.html"

    def get_success_url(self) -> str:
        return reverse("web:manage_web")


class ManagePreviewEmailEngagementDetailsView(PrivateWebDetailView):
    model = WebsiteEmail
    pk_url_kwarg = "pk"

    def render_to_response(self, context, **response_kwargs):
        template_name = self.object.previsualization_template
        context.update({"content": self.object.content, "preview": True})

        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=[template_name],
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


class ManageTermListView(PrivateWebListView):
    model = Term
    template_name = "management/list_terms.html"
    context_object_name = "terms"

    def get_queryset(self):
        return self.model._default_manager.all_terms_ready_newsletter()


class ManageTermUpdateView(PrivateWebUpdateView):
    model = Term
    template_name = "management/update_term.html"
    slug_field = "slug"
    fields = "__all__"
