from django.db.models import (
    SET_NULL,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    IntegerField,
    Model,
)

from apps.empresas.models import Company


class InstitutionalOrganization(Model):
    name = CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Institutional Organization"
        verbose_name_plural = "Institutional Organizations"
        db_table = "assets_institutional_organizations"

    def __str__(self):
        return self.name


class TopInstitutionalOwnership(Model):
    date = IntegerField(default=0)
    year = DateField(blank=True, null=True)
    company = ForeignKey(
        Company,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="top_institutional_ownership"
    )
    organization = ForeignKey(
        InstitutionalOrganization, on_delete=SET_NULL, null=True,
        blank=True, related_name="institution"
    )
    percentage_held = FloatField(default=0, blank=True, null=True)
    position = FloatField(default=0, blank=True, null=True)
    value = FloatField(default=0, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Top institutional owners"
        verbose_name_plural = "Top institutional owners"
        db_table = "assets_top_institutional_ownership"

    def __str__(self):
        return self.company.ticker + str(self.date)
