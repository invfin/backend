import json

from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONField,
    Model,
    TextField,
)
from django.urls import reverse

from src.empresas import constants
from src.empresas.managers import CompanyManager, CompanyUpdateLogManager
from src.general.mixins import BaseToAllMixin, CheckingsMixin
from src.periods.constants import PERIOD_FOR_YEAR


def default_dict():
    with open(constants.DEFAULT_JSON_CHECKS_FILE, "r") as checks_json:
        return json.load(checks_json)


class Company(Model, BaseToAllMixin, CheckingsMixin):
    ticker = CharField(max_length=30, unique=True, db_index=True)
    name = CharField(max_length=700, null=True, blank=True)
    currency = ForeignKey(
        "currencies.Currency",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    industry = ForeignKey(
        "industries_sectors.Industry",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    sector = ForeignKey(
        "industries_sectors.Sector",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    website = CharField(max_length=250, null=True, blank=True)
    state = CharField(max_length=250, null=True, blank=True)
    country = ForeignKey(
        "countries.Country",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    ceo = CharField(max_length=250, null=True, blank=True)
    image = CharField(max_length=250, null=True, blank=True)
    city = CharField(max_length=250, null=True, blank=True)
    employees = CharField(max_length=250, null=True, blank=True)
    address = CharField(max_length=250, null=True, blank=True)
    zip_code = CharField(max_length=250, null=True, blank=True)
    cik = CharField(max_length=250, null=True, blank=True)
    exchange = ForeignKey(
        "empresas.Exchange",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )
    cusip = CharField(max_length=250, null=True, blank=True)
    isin = CharField(max_length=250, null=True, blank=True)
    description = TextField(null=True, blank=True)
    ipoDate = CharField(max_length=250, null=True, blank=True)
    beta = FloatField(default=0, blank=True, null=True)
    is_trust = BooleanField(default=False)
    last_div = FloatField(default=0, blank=True, null=True)
    is_adr = BooleanField(default=False)
    is_fund = BooleanField(default=False)
    is_etf = BooleanField(default=False)
    no_incs = BooleanField(default=False)
    no_bs = BooleanField(default=False)
    no_cfs = BooleanField(default=False)
    description_translated = BooleanField(default=False)
    has_logo = BooleanField(default=False)
    updated = BooleanField(default=False)
    last_update = DateTimeField(null=True, blank=True)
    date_updated = BooleanField(default=False)
    has_error = BooleanField(default=False)
    error_message = TextField(null=True, blank=True)
    remote_image_imagekit = CharField(max_length=500, default="", blank=True)
    remote_image_cloudinary = CharField(max_length=500, default="", blank=True)
    checkings = JSONField(default=default_dict)
    need_parsing = BooleanField(default=False)

    objects = CompanyManager()

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "assets_companies"
        ordering = ["ticker"]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("screener:company", kwargs={"ticker": self.ticker})

    @property
    def full_name(self):
        return f"{self.ticker} {self.name}"

    @property
    def has_meta_image(self):
        if "has_meta_image" in self.checkings and self.has_checking("has_meta_image"):
            return True
        return bool(self.remote_image_imagekit or self.remote_image_cloudinary)

    @property
    def meta_image(self):
        return (
            self.remote_image_imagekit
            if self.remote_image_imagekit
            else self.remote_image_cloudinary
        )

    @property
    def most_recent_year(self):
        return self.inc_statements.latest().date  # type: ignore

    @property
    def has_institutions(self):
        return self.topinstitutionalownership_set.all().exists()  # type: ignore

    @property
    def has_ttm(self):
        return (
            self.inc_statements.filter(is_ttm=True).exists()  # type: ignore
            and self.balance_sheets.filter(is_ttm=True).exists()  # type: ignore
            and self.cf_statements.filter(is_ttm=True).exists()  # type: ignore
        )


class CompanyYahooQueryProxy(Company):
    class Meta:
        proxy = True

    @property
    def has_inc(self):
        return self.incomestatementyahooquery_set.all().exists()  # type: ignore

    @property
    def has_bs(self):
        return self.balancesheetyahooquery_set.all().exists()  # type: ignore

    @property
    def has_cf(self):
        return self.cashflowstatementyahooquery_set.all().exists()  # type: ignore

    @property
    def has_inc_quarter(self):
        return (
            self.incomestatementyahooquery_set.all()  # type: ignore
            .exclude(period__period=PERIOD_FOR_YEAR)
            .exists()
        )

    @property
    def has_bs_quarter(self):
        return (
            self.balancesheetyahooquery_set.all()  # type: ignore
            .exclude(period__period=PERIOD_FOR_YEAR)
            .exists()
        )

    @property
    def has_cf_quarter(self):
        return (
            self.cashflowstatementyahooquery_set.all()  # type: ignore
            .exclude(period__period=PERIOD_FOR_YEAR)
            .exists()
        )

    @property
    def has_key_stats(self):
        return self.keystatsyahooquery_set.all().exists()  # type: ignore


class CompanyYFinanceProxy(Company):
    class Meta:
        proxy = True

    @property
    def has_inc(self):
        return self.incomestatementyfinance_set.all().exists()  # type: ignore

    @property
    def has_bs(self):
        return self.balancesheetyfinance_set.all().exists()  # type: ignore

    @property
    def has_cf(self):
        return self.cashflowstatementyfinance_set.all().exists()  # type: ignore


class CompanyFinprepProxy(Company):
    class Meta:
        proxy = True

    @property
    def has_inc(self):
        return self.incomestatementfinprep_set.all().exists()  # type: ignore

    @property
    def has_bs(self):
        return self.balancesheetfinprep_set.all().exists()  # type: ignore

    @property
    def has_cf(self):
        return self.cashflowstatementfinprep_set.all().exists()  # type: ignore


class CompanyFinnhubProxy(Company):
    class Meta:
        proxy = True

    @property
    def has_statements(self):
        return self.statementsfinnhub_set.all().exists()  # type: ignore


class CompanyStatementsProxy(Company):
    class Meta:
        proxy = True


class CompanyStockPrice(Model):
    company_related = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="stock_prices",
    )
    date = IntegerField(default=0)
    year = DateTimeField(auto_now=True)
    price = FloatField(default=0, blank=True, null=True)
    data_source = CharField(
        max_length=100,
        choices=constants.DATA_SOURCES,
        default=constants.DATA_SOURCE_YFINANCE,
    )

    class Meta:
        get_latest_by = "date"
        ordering = ["-date"]
        verbose_name = "Stock price"
        verbose_name_plural = "Stock prices"
        db_table = "assets_companies_stock_prices"

    def __str__(self) -> str:
        return str(self.company_related) or "Has no company"

    def save(self, *args, **kwargs) -> None:
        self.date = self.year.year
        return super().save(*args, **kwargs)


class CompanyUpdateLog(Model):
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="company_log_historial",
    )
    date = DateTimeField(null=True, blank=True)
    where = CharField(max_length=250)
    had_error = BooleanField(default=False)
    error_message = TextField(default="", null=True)
    objects = CompanyUpdateLogManager()

    class Meta:
        get_latest_by = "date"
        ordering = ["-date"]
        verbose_name = "Logs"
        verbose_name_plural = "Logs"
        db_table = "assets_companies_updates_logs"

    def __str__(self) -> str:
        return str(self.company) or "Has no company"
