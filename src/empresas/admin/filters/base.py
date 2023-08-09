from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from src.periods import constants


class PeriodFilter(SimpleListFilter):
    title = "Period"
    parameter_name = "period"

    def lookups(self, request, model_admin):
        return constants.PERIODS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(period__period=self.value())
        return queryset


class HasQuarterFilter(SimpleListFilter):
    # Not efficient
    title = "Has quarters"

    parameter_name = "has_quarters"

    statements = []

    def get_related_statements(self):
        companies_id = set()
        for statement in self.statements:
            query_companies_id = statement.objects.filter(
                ~Q(period__period=constants.PERIOD_FOR_YEAR)
            ).values_list("company_id", flat=True)
            if query_companies_id:
                companies_id.update(list(query_companies_id))
        return list(companies_id)

    def lookups(self, request, model_admin):
        return ((True, True), (False, False))

    def queryset(self, request, queryset):
        companies_id = self.get_related_statements()
        if self.value() == "True":
            # If has_quarters=True
            return queryset.filter(id__in=companies_id)
        elif self.value() == "False":
            # If has_quarters=False
            return queryset.exclude(id__in=companies_id)


class NewCompanyToParseFilter(SimpleListFilter):
    title = "New company need parsing"

    parameter_name = "has_need_parsing"

    def lookups(self, request, model_admin):
        return (("True", True), ("False", False))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__contains="Need-parsing")
        else:
            return queryset.exclude(name__contains="Need-parsing")
