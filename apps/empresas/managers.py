import random

from django.db.models import (
    Count,
    F,
    Manager,
    Q,
    Subquery,
    OuterRef,
)


class CompanyManager(Manager):
    """
    TODO
    Create querysets or managers for statements to return quarters and for year separately
    https://docs.djangoproject.com/en/dev/topics/db/managers/#don-t-filter-away-any-results-in-this-type-of-manager-subclass
    """

    def only_essential(self):
        return self.only(
            "ticker",
            "name",
            "sector",
            "website",
            "state",
            "country",
            "ceo",
            "image",
            "city",
            "employees",
            "address",
            "zip_code",
            "cik",
            "cusip",
            "isin",
            "description",
            "ipoDate",
        )

    def prefetch_historical_data(self):
        return self.prefetch_related(
            "inc_statements",
            "balance_sheets",
            "cf_statements",
            "rentability_ratios",
            "liquidity_ratios",
            "margins",
            "fcf_ratios",
            "per_share_values",
            "non_gaap_figures",
            "operation_risks_ratios",
            "ev_ratios",
            "growth_rates",
            "efficiency_ratios",
            "price_to_ratios",
        )

    def fast_full(self):
        return self.prefetch_historical_data().only(
            "ticker",
            "name",
            "sector",
            "website",
            "state",
            "country",
            "ceo",
            "image",
            "city",
            "employees",
            "address",
            "zip_code",
            "cik",
            "cusip",
            "isin",
            "description",
            "ipoDate",
        )

    def get_random(self, query=None):
        query = query if query else self.all()
        return random.choice(list(query))

    def companies_by_main_exchange(self, name=None):
        return self.filter(exchange__main_org__name=name).exclude(name__contains="Need-parsing")

    def clean_companies(self):
        return self.filter(no_incs=False, no_bs=False, no_cfs=False).exclude(name__contains="Need-parsing")

    def clean_companies_by_main_exchange(self, name=None):
        return self.filter(no_incs=False, no_bs=False, no_cfs=False, exchange__main_org__name=name).exclude(
            name__contains="Need-parsing"
        )

    def complete_companies_by_main_exchange(self, name=None):
        return self.filter(
            no_incs=False, no_bs=False, no_cfs=False, description_translated=True, exchange__main_org__name=name
        ).exclude(name__contains="Need-parsing")

    def get_similar_companies(self, sector_id, industry_id):
        return self.filter(
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            sector_id=sector_id,
            industry_id=industry_id,
        ).exclude(name__contains="Need-parsing")

    def random_clean_company(self):
        return self.get_random(self.clean_companies())

    def random_clean_company_by_main_exchange(self, name=None):
        return self.get_random(self.clean_companies_by_main_exchange(name))

    def random_complete_companies_by_main_exchange(self, name=None):
        return self.get_random(self.complete_companies_by_main_exchange(name))

    def clean_companies_to_update(self, name=None):
        return self.filter(
            no_incs=False, no_bs=False, no_cfs=False, exchange__main_org__name=name, updated=False, has_error=False
        )

    def get_random_most_visited_clean_company(self):
        return self.get_random(
            self.filter(no_incs=False, no_bs=False, no_cfs=False, has_error=False, description_translated=True)
            .exclude(name__contains="Need-parsing")
            .annotate(
                visited_by_user=Count("usercompanyvisited"),
                visited_by_visiteur=Count("visiteurcompanyvisited"),
                total_visits=F("visited_by_user") + F("visited_by_visiteur"),
            )
            .order_by("total_visits")
        )

    def get_most_visited_companies(self):
        """
        Based on most visited companies
        """
        return (
            self.filter(no_incs=False, no_bs=False, no_cfs=False)
            .exclude(name__contains="Need-parsing")
            .annotate(
                visited_by_user=Count("usercompanyvisited"),
                visited_by_visiteur=Count("visiteurcompanyvisited"),
                total_visits=F("visited_by_user") + F("visited_by_visiteur"),
            )
            .order_by("total_visits")
        )

    def related_companies_most_visited(
        self,
        sector,
        exchage,
        industry,
        country,
    ):
        return (
            self.filter(
                Q(sector__id__in=sector)
                | Q(exchange__id__in=exchage)
                | Q(industry__id__in=industry)
                | Q(country__id__in=country),
                no_incs=False,
                no_bs=False,
                no_cfs=False,
            )
            .exclude(name__contains="Need-parsing")
            .annotate(
                visited_by_user=Count("usercompanyvisited"),
                visited_by_visiteur=Count("visiteurcompanyvisited"),
                total_visits=F("visited_by_user") + F("visited_by_visiteur"),
            )
            .order_by("total_visits")
        )

    def filter_checkings(self, check: str, has_it: bool):
        checking = f"has_{check}"
        state = "yes" if has_it else "no"
        return (
            self.filter(**{f"checkings__{checking}__state": state})
            .exclude(name__contains="Need-parsing")
            .order_by("exchange__main_org__order")
        )

    def filter_checkings_not_seen(self, check: str):
        return (
            self.filter(**{f"checkings__has_{check}__state": "no", f"checkings__has_{check}__time": ""})
            .exclude(name__contains="Need-parsing")
            .order_by("exchange__main_org__order")
        )


class CompanyUpdateLogManager(Manager):
    pass
