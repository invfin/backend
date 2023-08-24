from typing import Any, Dict, Optional

from django.db.models import Count, F, Manager, Prefetch, Q

from src.general.managers import BaseManager, BaseQuerySet


class CompanyQuerySet(BaseQuerySet):
    def existing_companies_by_exchange_importance(self):
        exchanges_order = "exchange__main_org__order"
        return self.exclude(name__contains="Need-parsing").order_by(exchanges_order)

    def prefetch_yearly_historical_data(self, **kwargs):
        lookup_filter = {"company__ticker": kwargs["ticker"]} if "ticker" in kwargs else {}

        return self.prefetch_related(
            Prefetch(
                "inc_statements",
                queryset=self.model.inc_statements.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "balance_sheets",
                queryset=self.model.balance_sheets.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "cf_statements",
                queryset=self.model.cf_statements.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "rentability_ratios",
                queryset=self.model.rentability_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "liquidity_ratios",
                queryset=self.model.liquidity_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "margins",
                queryset=self.model.margins.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "fcf_ratios",
                queryset=self.model.fcf_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "per_share_values",
                queryset=self.model.per_share_values.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "non_gaap_figures",
                queryset=self.model.non_gaap_figures.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "operation_risks_ratios",
                queryset=self.model.operation_risks_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "ev_ratios",
                queryset=self.model.ev_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "growth_rates",
                queryset=self.model.growth_rates.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "efficiency_ratios",
                queryset=self.model.efficiency_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
            Prefetch(
                "price_to_ratios",
                queryset=self.model.price_to_ratios.rel.related_model.objects.yearly(
                    False, **lookup_filter
                ),
            ),
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

    def select_related_information(self):
        return self.select_related(
            "currency",
            "industry",
            "sector",
            "country",
            "exchange",
        )


class CompanyManager(BaseManager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db)

    def select_related_information(self):
        return self.get_queryset().select_related_information()

    def prefetch_yearly_historical_data(self, **kwargs):
        lookup_filter = {"company__ticker": kwargs["ticker"]} if "ticker" in kwargs else {}
        return (
            self.get_queryset()
            .prefetch_yearly_historical_data(**lookup_filter)
            .get(**lookup_filter)
        )

    def fast_full(self, **kwargs):
        return self.get_queryset().prefetch_historical_data().only_essential().get(**kwargs)

    def clean_companies_by_main_exchange(self, name=None):
        return self.filter(
            no_incs=False, no_bs=False, no_cfs=False, exchange__main_org__name=name
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

    def get_random_most_visited_clean_company(self, exclude: Optional[Dict[str, Any]] = None):
        exclude = exclude or {}
        return self.get_random(
            self.filter(
                no_incs=False,
                no_bs=False,
                no_cfs=False,
                has_error=False,
                description_translated=True,
                exchange__main_org__name="Estados Unidos",
            )
            .exclude(name__contains="Need-parsing", **exclude)
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

    def filter_checking(self, checking: str, has_it: bool):
        return (
            super()
            .filter_checking(checking, has_it)
            .exclude(name__contains="Need-parsing")
            .order_by("exchange__main_org__order")
        )

    def filter_checking_not_seen(self, checking: str):
        queryset = super().filter_checking_not_seen(checking)
        return queryset.existing_companies_by_exchange_importance()  # type: ignore

    def api_query(self):
        return self.get_queryset().select_related_information().prefetch_historical_data()


class CompanyUpdateLogManager(Manager):
    pass
