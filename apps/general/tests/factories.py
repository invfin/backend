from apps.general.models import Tag, Category, Sector, Industry, Country, Currency
from apps.general.tests.data import (
    TAGS,
    CATEGORIES,
    COUNTRIES,
    CURRENCIES,
    SECTORS,
    INDUSTRIES
)


class GenerateGeneralExample:
    tags = Tag.objects.all()
    categories = Category.objects.all()
    countries = Country.objects.all()
    currencies = Currency.objects.all()
    sectors = Sector.objects.all()
    industries = Industry.objects.all()

    @classmethod
    def generate_tags(cls):
        for info in TAGS:
            Tag.objects.get_or_create(**info)

    @classmethod
    def generate_categories(cls):
        for info in CATEGORIES:
            Category.objects.get_or_create(**info)

    @classmethod
    def generate_countries(cls):
        for info in COUNTRIES:
            Country.objects.get_or_create(**info)

    @classmethod
    def generate_currencies(cls):
        for info in CURRENCIES:
            Currency.objects.get_or_create(**info)

    @classmethod
    def generate_sectors(cls):
        for info in SECTORS:
            Sector.objects.get_or_create(**info)

    @classmethod
    def generate_industries(cls):
        for info in INDUSTRIES:
            Industry.objects.get_or_create(**info)
    
    @classmethod
    def generate_all(cls):
        cls.generate_tags()
        cls.generate_categories()
        cls.generate_countries()
        cls.generate_currencies()
        cls.generate_sectors()
        cls.generate_industries()
