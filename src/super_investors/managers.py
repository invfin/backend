from django.db.models import (
    Case,
    ExpressionWrapper,
    F,
    Manager,
    TextField,
    Value,
    When,
)

from src.periods.models import Period


class SuperinvestorManager(Manager):
    def current_positions(self, pk):
        current_period = Period.objects.earliest()
        return self.get(id=pk).history.filter(period_related=current_period)

    def resume_current_positions(self, id: int):
        history = (
            self.get(id=id)
            .history.prefetch_related(
                "period_related",
                "company",
                "company__sector",
            )
            .all()
        )
        all_companies = (
            history.order_by()
            .values("company", "company_name")
            .distinct("company", "company_name")
        )[:5]
        portfolio = []
        for company in all_companies:
            query_company_history = (
                history.filter(**company, shares__gt=0)
                .annotate(
                    image=ExpressionWrapper(
                        Case(
                            When(
                                company__isnull=False,
                                then=F("company__image"),
                            ),
                            default=Value(""),
                            output_field=TextField(),
                        ),
                        output_field=TextField(),
                    ),
                    name=ExpressionWrapper(
                        Case(
                            When(
                                company__isnull=False,
                                then=F("company__name"),
                            ),
                            default=F("company_name"),
                            output_field=TextField(),
                        ),
                        output_field=TextField(),
                    ),
                )
                .values("name", "image")
            )
            portfolio.append(query_company_history.last())
        return portfolio

    def all_buys(self):
        pass

    def all_sells(self):
        pass


class SuperinvestorHistoryManager(Manager):
    def company_in_current_portfolios(self, company_id):
        current_period = Period.objects.earliest()
        return self.filter(period_related=current_period, company_id=company_id)
