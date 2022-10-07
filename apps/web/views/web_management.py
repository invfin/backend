from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from apps.general.utils import HostChecker
from apps.public_blog.models import WritterProfile
from apps.seo.views import SEOTemplateView
from apps.escritos.models import Term

from apps.web.models import WebsiteLegalPage, WebsiteEmail
from apps.web.forms import ContactForm, WebEmailForm


class BasePrivateWebView(UserPassesTestMixin):
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


class ManagementWebView(PrivateWebTemplateView):
    template_name = "management/inicio.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["models"] =
    #     return context


class ManagementTermListView(PrivateWebListView):
    model = Term
    template_name = "management/inicio_term.html"
    context_object_name = "terms"


class ManagementTermDetailView(PrivateWebUpdateView):
    model = Term
    template_name = "management/details_term.html"
    slug_field = "slug"
    fields = "__all__"


class WebEngagementView(PrivateWebListView):
    template_name = "engagement/email_management.html"
    model = WebsiteEmail
    context_object_name = "web_emails"


class CreateWebEmailView(PrivateWebCreateView):
    form_class = WebEmailForm
    template_name = "engagement/mandar_emails.html"

    def get_success_url(self) -> str:
        return reverse("web:manage_engagement_web")
