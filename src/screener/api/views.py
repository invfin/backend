import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView

import yahooquery as yq

from src.empresas.models import Company
from src.empresas.outils.company import CompanyData
from src.empresas.outils.valuations import discounted_cashflow

from ..forms import UserCompanyObservationForm
from ..models import UserCompanyObservation, UserScreenerMediumPrediction, UserScreenerSimplePrediction, YahooScreener

User = get_user_model()


class CompanyFODAListView(ListView):
    model = UserCompanyObservation
    template_name = "empresas/company_parts/foda/foda_parts.html"
    context_object_name = "foda_analysis"

    def get_queryset(self):
        return UserCompanyObservation.objects.filter(company__id=self.kwargs["company_id"])


def get_company_price(request, ticker):
    prices = CompanyData.get_most_recent_price(ticker)["current_price"]
    return render(
        request,
        "headers/company_price.html",
        {
            "prices": prices,
        },
    )


def get_company_news(request, ticker):
    # company = Company.objects.get(ticker=ticker)
    # news = RetrieveCompanyData(company).get_news()
    news = []
    return render(
        request,
        "empresas/company_parts/resume/news.html",
        {
            "show_news": news,
        },
    )


def get_company_valuation(request, ticker):
    company = Company.objects.get(ticker=ticker)
    company_valuation = CompanyData(company).get_ratios_information()
    return render(
        request,
        "empresas/company_parts/valuations/response.html",
        {
            "company_valuation": company_valuation,
        },
    )


def retreive_yahoo_screener_info(request, query):
    yahoo = yq.Screener().get_screeners(query)
    context = {"yahoo": yahoo[query]["quotes"]}
    return render(request, "yahoo-screeners/screener-data.html", context)


def retreive_top_lists(request):
    yahoo = yq.Screener().get_screeners(["most_actives", "day_gainers", "day_losers"], 5)
    extra = {"positive": "text-success", "negative": "text-danger"}
    url = "/screener/analisis-de/"
    day_gainers = {
        "title": "Mayor aumento de precio",
        "subtitle": "day_gainers",
        "slug": YahooScreener.objects.get(yq_name="day_gainers").slug,
        "extra": extra,
        "url": url,
        "data": yahoo["day_gainers"]["quotes"],
    }
    day_losers = {
        "title": "Mayor disminución de precio",
        "subtitle": "day_losers",
        "slug": YahooScreener.objects.get(yq_name="day_losers").slug,
        "extra": extra,
        "url": url,
        "data": yahoo["day_losers"]["quotes"],
    }
    most_actives = {
        "title": "Más activos",
        "subtitle": "most_actives",
        "slug": YahooScreener.objects.get(yq_name="most_actives").slug,
        "extra": extra,
        "url": url,
        "data": yahoo["most_actives"]["quotes"],
    }

    gainers_actives_losers = [day_gainers, most_actives, day_losers]
    return render(
        request,
        "yahoo-screeners/top-lists.html",
        {
            "gainers_actives_losers": gainers_actives_losers,
        },
    )


def return_similar_companies_screener(request, sector_id, industry_id):
    return render(
        request,
        "empresas/company_parts/relationships/relations.html",
        {
            "similar_companies": Company.objects.get_similar_companies(sector_id, industry_id),
            "previous_ticker": request.GET.get("extra"),
        },
    )


class CompanyObservationFormView(FormView):
    form_class = UserCompanyObservationForm
    template_name = "empresas/company_parts/foda/foda_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_ticker"] = self.request.GET["company_ticker"]
        return context

    def form_valid(self, form):
        company_ticker = self.request.POST["company_ticker"]
        user = User.objects.get_or_create_quick_user(self.request)
        model = form.save()
        model.user = user
        company = Company.objects.get(ticker=company_ticker)
        model.company = company
        model.save(update_fields=["user", "company"])
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshObservationsCompany"})


def suggest_list_search_companies(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        companies_availables = Company.objects.filter(
            Q(name__icontains=query) | Q(ticker__icontains=query),
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        ).only("name", "ticker")[:10]

        results = []
        for company in companies_availables:
            result = f"{company.name} ({company.ticker})"
            results.append(result)

        data = json.dumps(results)
    return HttpResponse(data, "application/json")


def medium_valuation_view(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    user = request.user if request.user.is_authenticated else None
    if is_ajax and request.method == "POST":
        data = json.load(request)

        opt_growth = float(data.get("complex_opt_growth", 0).replace(",", "."))
        neu_growth = float(data.get("complex_neu_growth", 0).replace(",", "."))
        pes_growth = float(data.get("complex_pes_growth", 0).replace(",", "."))
        company_id = data.get("company_id")
        opt_margin = float(data.get("complex_opt_margin", 0).replace(",", "."))
        neu_margin = float(data.get("complex_neu_margin", 0).replace(",", "."))
        pes_margin = float(data.get("complex_pes_margin", 0).replace(",", "."))
        opt_buyback = float(data.get("complex_opt_buyback", 0).replace(",", "."))
        neu_buyback = float(data.get("complex_neu_buyback", 0).replace(",", "."))
        pes_buyback = float(data.get("complex_pes_buyback", 0).replace(",", "."))
        opt_fcf_margin = float(data.get("complex_opt_fcf_margin", 0).replace(",", "."))
        neu_fcf_margin = float(data.get("complex_neu_fcf_margin", 0).replace(",", "."))
        pes_fcf_margin = float(data.get("complex_pes_fcf_margin", 0).replace(",", "."))

        the_company = Company.objects.get(id=company_id)
        latest_inc = the_company.inc_statements.latest()

        last_revenue = latest_inc.revenue
        average_shares_out = latest_inc.weighted_average_shares_outstanding

        UserScreenerMediumPrediction.objects.create(
            user=user,
            company=the_company,
            optimistic_growth=opt_growth,
            neutral_growth=neu_growth,
            pesimistic_growth=pes_growth,
            optimistic_margin=opt_margin,
            neutral_margin=neu_margin,
            pesimistic_margin=pes_margin,
            optimistic_buyback=opt_buyback,
            neutral_buyback=neu_buyback,
            pesimistic_buyback=pes_buyback,
            optimistic_fcf_margin=opt_fcf_margin,
            neutral_fcf_margin=neu_fcf_margin,
            pesimistic_fcf_margin=pes_fcf_margin,
        )

        opt_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=opt_growth,
            net_income_margin=opt_margin,
            fcf_margin=opt_fcf_margin,
            buyback=opt_buyback,
            average_shares_out=average_shares_out,
        )
        neu_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=neu_growth,
            net_income_margin=neu_margin,
            fcf_margin=opt_fcf_margin,
            buyback=neu_buyback,
            average_shares_out=average_shares_out,
        )
        pes_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=pes_growth,
            net_income_margin=pes_margin,
            fcf_margin=opt_fcf_margin,
            buyback=pes_buyback,
            average_shares_out=average_shares_out,
        )
        return JsonResponse(
            {
                "complex_opt_valuation": opt_valuation,
                "complex_neu_valuation": neu_valuation,
                "complex_pes_valuation": pes_valuation,
            }
        )


def simple_valuation_view(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    user = request.user if request.user.is_authenticated else None
    if is_ajax and request.method == "POST":
        data = json.load(request)

        opt_growth = float(data.get("opt_grow", 0).replace(",", "."))
        neu_growth = float(data.get("neu_grow", 0).replace(",", "."))
        pes_growth = float(data.get("pes_grow", 0).replace(",", "."))
        company_id = data.get("comp")
        # buyback = float(data.get('buyback', 0).replace(',', '.'))

        the_company = Company.objects.get(id=company_id)
        latest_inc = the_company.inc_statements.latest()
        latest_margin = the_company.margins.latest()
        last_revenue = latest_inc.revenue
        average_shares_out = latest_inc.weighted_average_shares_outstanding
        net_income_margin = latest_margin.net_income_margin
        fcf_margin = latest_margin.fcf_margin
        buyback = the_company.growth_rates.latest().shares_buyback

        UserScreenerSimplePrediction.objects.create(
            user=user,
            company=the_company,
            optimistic_growth=opt_growth,
            neutral_growth=neu_growth,
            pesimistic_growth=pes_growth,
        )

        opt_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=opt_growth,
            net_income_margin=net_income_margin,
            fcf_margin=fcf_margin,
            buyback=buyback,
            average_shares_out=average_shares_out,
        )
        neu_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=neu_growth,
            net_income_margin=net_income_margin,
            fcf_margin=fcf_margin,
            buyback=buyback,
            average_shares_out=average_shares_out,
        )
        pes_valuation = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=pes_growth,
            net_income_margin=net_income_margin,
            fcf_margin=fcf_margin,
            buyback=buyback,
            average_shares_out=average_shares_out,
        )

        return JsonResponse(
            {"opt_valuation": opt_valuation, "neu_valuation": neu_valuation, "pes_valuation": pes_valuation}
        )
