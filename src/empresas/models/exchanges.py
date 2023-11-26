from django.db.models import SET_NULL, CharField, ForeignKey, Model, PositiveIntegerField

from src.empresas import constants


class ExchangeOrganisation(Model):
    name = CharField(max_length=250, default="", blank=True)
    image = CharField(max_length=250, default="", blank=True)
    sub_exchange1 = CharField(max_length=250, default="", blank=True)
    sub_exchange2 = CharField(max_length=250, default="", blank=True)
    order = PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Organisation exchange"
        verbose_name_plural = "Organisation exchanges"
        db_table = "assets_exchanges_organisations"

    def __str__(self)->str:
        return self.name or str(self.pk)


class Exchange(Model):
    exchange_ticker = CharField(max_length=30, default="", blank=True)
    exchange = CharField(max_length=250, default="", blank=True)
    country = ForeignKey("countries.Country", on_delete=SET_NULL, null=True, blank=True)
    main_org = ForeignKey(ExchangeOrganisation, on_delete=SET_NULL, null=True, blank=True)
    data_source = CharField(
        max_length=100, choices=constants.DATA_SOURCES, default=constants.DATA_SOURCE_FINPREP
    )

    class Meta:
        ordering = ["-exchange_ticker"]
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"
        db_table = "assets_exchanges"

    def __str__(self):
        return self.exchange_ticker or str(self.pk)

    @property
    def num_emps(self):
        return self.companies.all().count()
