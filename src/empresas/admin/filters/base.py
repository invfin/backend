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
            query_companies_id = statement.objects.filter(~Q(period__period=constants.PERIOD_FOR_YEAR)).values_list(
                "company_id", flat=True
            )
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


class JSONFieldFilter(SimpleListFilter):
    """ """

    def __init__(self, *args, **kwargs):
        super(JSONFieldFilter, self).__init__(*args, **kwargs)

        assert hasattr(self, "title"), 'Class {} missing "title" attribute'.format(self.__class__.__name__)
        assert hasattr(self, "parameter_name"), 'Class {} missing "parameter_name" attribute'.format(
            self.__class__.__name__
        )
        assert hasattr(self, "json_field_name"), 'Class {} missing "json_field_name" attribute'.format(
            self.__class__.__name__
        )
        assert hasattr(
            self, "json_field_property_name"
        ), 'Class {} missing "json_field_property_name" attribute'.format(self.__class__.__name__)

    def lookups(self, request, model_admin):
        """
        # Improvemnt needed: if the size of jsonfield is large and there are lakhs of row
        """
        if "__" in self.json_field_property_name:  # NOTE: this will cover only one nested level
            keys = self.json_field_property_name.split("__")
            field_value_set = set(
                data[keys[0]][keys[1]]
                for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        else:
            field_value_set = set(
                data[self.json_field_property_name]
                for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
            return [(v, v) for v in field_value_set]

    def queryset(self, request, queryset):
        if self.value():
            json_field_query = {"{}__{}".format(self.json_field_name, self.json_field_property_name): self.value()}
            return queryset.filter(**json_field_query)
        else:
            return queryset


# Now Extend this class to create custom admin filter for JSON field properties.


# admin.py
class AgeFilter(JSONFieldFilter):
    """ """

    title = "Age"  # for admin sidebar (above the filter options)
    parameter_name = "jsonage"  # Parameter for the filter that will be used in the URL query
    json_field_name = "jsonfield"
    json_field_property_name = "age"  # property/field in json data
