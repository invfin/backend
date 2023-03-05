from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from src.escritos.forms import TermAndTermContentForm, term_content_formset
from src.escritos.models import Term
from src.seo.views import SEOViewMixin
from src.web.forms import AutomaticNewsletterForm, WebEmailForm
from src.web.models import WebsiteEmail


class BasePrivateWebView(LoginRequiredMixin, UserPassesTestMixin, SEOViewMixin):
    private_view = True

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

    def successful_return(self) -> HttpResponse:
        messages.success(self.request, "Guardado correctamente")
        return HttpResponse(status=204, headers={"HX-Trigger": "showMessageSuccess"})

    def get_success_url(self) -> str:
        return reverse("web:manage_web")

    def form_valid(self, form) -> HttpResponse:
        form.save()
        if self.request.META.get("HTTP_HX_REQUEST"):
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
        context.update({**self.object.email_serialized, "preview": True})

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
        return self.model._default_manager.cleaning_requested()


class ManageTermUpdateView(PrivateWebDetailView):
    model = Term
    template_name = "management/update_term.html"
    slug_field = "slug"

    def get_success_url(self) -> str:
        return reverse("web:manage_all_terms")

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["formset_content"] = term_content_formset(instance=self.object)
        context["form"] = TermAndTermContentForm(instance=self.object)
        return context

    def save_all(self, form, formset, request):
        modify_checking = True if "save_definetly" in request.POST else False
        form.save(modify_checking=modify_checking)
        formset.save()
        messages.success(request, "Guardado correctamente")
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args: str, **kwargs) -> HttpResponse:
        object = self.get_object()
        formset = term_content_formset(request.POST, instance=object)
        form = TermAndTermContentForm(request.POST, instance=object)
        if all([form.is_valid(), formset.is_valid()]):
            return self.save_all(form, formset, request)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
