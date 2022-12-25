from src.general.filters import JSONFieldFilter


class TermsHasRequestImprovementFilter(JSONFieldFilter):
    title = "Has request improvement"  # for admin sidebar (above the filter options)
    parameter_name = "reimprovement"  # Parameter for the filter that will be used in the URL query
    json_field_name = "checkings"
    json_field_property_name = "has_request_improvement__state"  # property/field in json data

    def lookups(self, request, model_admin):
        return [("yes", True), ("no", False)]


class TermsHasInformationCleanFilter(JSONFieldFilter):
    title = "Has clean information"  # for admin sidebar (above the filter options)
    parameter_name = "cleaninfo"  # Parameter for the filter that will be used in the URL query
    json_field_name = "checkings"
    json_field_property_name = "has_information_clean__state"  # property/field in json data

    def lookups(self, request, model_admin):
        return [("yes", True), ("no", False)]
