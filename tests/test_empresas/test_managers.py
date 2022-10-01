import pytest

from apps.empresas.models import Company


@pytest.mark.django_db
@pytest.mark.usefixtures("empresas_manager_companies")
class TestCompanyManagers:
    def test_filter_checkings(self):
        assert [self.zinga] == list(Company.objects.filter_checkings("institutionals", True))
        assert [self.apple, self.google, self.louis] == list(Company.objects.filter_checkings("institutionals", False))

    def test_companies_by_main_exchange(self):
        assert [self.apple, self.google, self.zinga] == list(
            Company.objects.companies_by_main_exchange("Estados Unidos")
        )

    def test_clean_companies(self):
        assert [self.apple, self.google, self.zinga] == list(Company.objects.clean_companies())

    def test_clean_companies_by_main_exchange(self):
        assert [self.apple, self.google, self.zinga] == list(
            Company.objects.clean_companies_by_main_exchange("Estados Unidos")
        )

    def test_complete_companies_by_main_exchange(self):
        assert [self.apple, self.google] == list(Company.objects.complete_companies_by_main_exchange("Estados Unidos"))

    def test_get_similar_companies(self):
        assert [self.apple, self.google] == list(
            Company.objects.get_similar_companies(self.sector.id, self.industry.id)
        )

    def test_clean_companies_to_update(self):
        assert [self.google] == list(Company.objects.clean_companies_to_update("Estados Unidos"))
