from django.db.models import Manager


class SuperinvestorManager(Manager):
    def current_positions(self, pk):
        from apps.super_investors.models import Period
        current_period = Period.objects.earliest()
        return self.get(id=pk).history.filter(period_related=self.current_period)

    def resume_current_positions(self):
        pass

    def all_buys(self):
        pass

    def all_sells(self):
        pass


class SuperinvestorHistoryManager(Manager):
    def company_in_current_portfolios(self, company_id):
        from apps.super_investors.models import Period
        current_period = Period.objects.earliest()
        return self.filter(period_related=self.current_period, company_id=company_id)
