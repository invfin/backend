from django.contrib.admin import SimpleListFilter


TASK_METHODS = (
    ("create_financials_yfinance", "create_financials_yfinance"),
    ("create_financials_finnhub", "create_financials_finnhub"),
    ("create_key_stats_yahooquery", "create_key_stats_yahooquery"),
    ("create_institutionals_yahooquery", "create_institutionals_yahooquery"),
    ("create_financials_yahooquery", "create_financials_yahooquery"),
    ("add_logo", "add_logo"),
    ("add_description", "add_description"),
)


class CompanyLogsFilter(SimpleListFilter):
    title = "Log place"
    parameter_name = "log_place"

    def lookups(self, request, model_admin):
        return TASK_METHODS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(where=self.value())
        return queryset
