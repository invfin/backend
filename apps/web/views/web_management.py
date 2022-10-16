from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse

from apps.escritos.models import Term
from apps.web.models import WebsiteEmail
from apps.web.forms import WebEmailForm
from apps.web.tasks import send_email_engagement_task
from apps.seo.views import SEOViewMixin
from apps.web.outils.engagement import EngagementMachine
from apps.web import constants
from apps.socialmedias import constants as socialmedias_constants


class BasePrivateWebView(UserPassesTestMixin, SEOViewMixin):
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


class ManageWebView(PrivateWebListView):
    model = WebsiteEmail
    template_name = "management/inicio.html"
    context_object_name = "web_emails"


class ManageEmailEngagementListView(PrivateWebListView):
    template_name = "engagement/list_emails.html"
    model = WebsiteEmail
    context_object_name = "web_emails"

    def get_context_data(self, **kwargs):
        EngagementMachine().create_newsletter(
            constants.CONTENT_FOR_NEWSLETTER,
            socialmedias_constants.TERM,
            constants.WHOM_TO_SEND_EMAIL_ALL,
        )
        return super().get_context_data(**kwargs)


class ManageEmailEngagementUpdateView(PrivateWebUpdateView):
    model = WebsiteEmail
    form_class = WebEmailForm
    template_name = "engagement/form_email.html"
    pk_url_kwarg = "pk"

    def get_success_url(self) -> str:
        return reverse("web:list_emails_engagement")


class ManageEmailEngagementCreateView(PrivateWebCreateView):
    form_class = WebEmailForm
    template_name = "engagement/form_email.html"

    def get_success_url(self) -> str:
        return reverse("web:list_emails_engagement")


def send_email_management(request, email_id: int):
    if request.POST:
        send_email_engagement_task.delay(email_id)
        return HttpResponse(status=204, headers={"HX-Trigger": "showMessageSuccess"})


class ManageTermListView(PrivateWebListView):
    model = Term
    template_name = "management/list_terms.html"
    context_object_name = "terms"


class ManageTermUpdateView(PrivateWebUpdateView):
    model = Term
    template_name = "management/update_term.html"
    slug_field = "slug"
    fields = "__all__"
