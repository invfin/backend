from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
    View,
)

from src.escritos.models import Term, TermsRelatedToResume
from src.preguntas_respuestas.models import Question
from src.promotions.models import Promotion
from src.public_blog.models import PublicBlog
from src.seo.mixins import SEOViewMixin


def redirect_old_urls(request, ques_slug=False, term_slug=False, publs_slug=False):
    if ques_slug is False and term_slug is False:
        model = PublicBlog.objects
        slug = publs_slug

    elif term_slug is False and publs_slug is False:
        model = Question.objects
        slug = ques_slug

    elif publs_slug is False and ques_slug is False:
        model = Term.objects
        slug = term_slug

    model_filtered = model.filter(Q(title__icontains=slug) | Q(slug__icontains=slug))
    if model_filtered.exists():
        redirect_to = model_filtered[0].get_absolute_url()
    else:
        second_model = Term.objects.filter(Q(title__icontains=slug) | Q(slug__icontains=slug))
        if second_model.exists():
            redirect_to = second_model[0].get_absolute_url()
        else:
            old_url = TermsRelatedToResume.objects.filter(
                Q(term_to_delete__slug__icontains=slug)
            )
            if old_url.exists():
                redirect_to = old_url[0].get_absolute_url()
            else:
                redirect_to = "escritos:glosario"
    return redirect(redirect_to)


class PromotionRedirectView(RedirectView):
    permanent = False

    def save_promotion_data(self, slug):
        model = Promotion.objects.get(slug=slug)
        return model.full_url

    def get(self, request, *args, **kwargs):
        slug = request.GET.kwargs["slug"]
        url = self.save_promotion_data(slug)
        return HttpResponseRedirect(url)


@transaction.non_atomic_requests
async def robots_txt(_):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class SEOListView(SEOViewMixin, ListView):
    pass


class SEODetailView(SEOViewMixin, DetailView):
    pass


class SEOView(SEOViewMixin, View):
    pass


class SEOFormView(SEOViewMixin, FormView):
    pass


class SEOTemplateView(SEOViewMixin, TemplateView):
    pass


class SEOCreateView(SEOViewMixin, CreateView):
    pass
