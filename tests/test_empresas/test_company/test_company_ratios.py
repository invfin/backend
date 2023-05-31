import time
from unittest import skip

from django.test import TestCase

from bfet import DjangoTestingModel
import vcr

from src.empresas.models import Company
from src.empresas.outils.data_management.update.update import UpdateCompany
from tests.data.empresas.finprep import finprep_data as data

company_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("Don't want to test")
class TestScrapCompanyInfo(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.company = DjangoTestingModel.create(Company)
        cls.company_update = UpdateCompany(cls.company)
        cls.company.inc_statements.create(date=2018)
        cls.zinga = DjangoTestingModel.create(Company, ticker="ZNGA")

    @company_vcr.use_cassette
    def test_need_update(self):
        self.assertFalse(self.company_update.needs_update())
        company2_update = UpdateCompany(self.company)
        self.company.inc_statements.create(date=2021)
        self.assertTrue(company2_update.needs_update())

    def test_all_data(self):
        current_data = self.company_update.generate_current_data(
            data.INCOME_STATEMENT, data.BALANCE_SHEET, data.CASHFLOW_STATEMENT
        )
        last_year_data = self.company_update.generate_last_year_data(
            data.INCOME_STATEMENT, data.BALANCE_SHEET, data.CASHFLOW_STATEMENT
        )

        all_data = current_data
        all_data.update(last_year_data)

        main_ratios = self.company_update.calculate_main_ratios(all_data)
        all_data.update(main_ratios)

        fcf_ratio = self.company_update.calculate_fcf_ratio(current_data)
        all_data.update(fcf_ratio)

        ps_value = self.company_update.calculate_ps_value(all_data)
        all_data.update(ps_value)

        company_growth = self.company_update.calculate_company_growth(all_data)
        all_data.update(company_growth)

        non_gaap = self.company_update.calculate_non_gaap(all_data)
        all_data.update(non_gaap)

        price_to_ratio = self.company_update.calculate_price_to_ratio(all_data)

        eficiency_ratio = self.company_update.calculate_eficiency_ratio(all_data)
        enterprise_value_ratio = self.company_update.calculate_enterprise_value_ratio(all_data)

        liquidity_ratio = self.company_update.calculate_liquidity_ratio(all_data)
        margin_ratio = self.company_update.calculate_margin_ratio(all_data)

        operation_risk_ratio = self.company_update.calculate_operation_risk_ratio(all_data)

        rentability_ratios = self.company_update.calculate_rentability_ratios(all_data)

        assert self.company.inc_statements.count() == 1
        assert self.company.stock_prices.count() == 0
        assert self.company.rentability_ratios.count() == 0
        assert self.company.liquidity_ratios.count() == 0
        assert self.company.margins.count() == 0
        assert self.company.fcf_ratios.count() == 0
        assert self.company.per_share_values.count() == 0
        assert self.company.non_gaap_figures.count() == 0
        assert self.company.operation_risks_ratios.count() == 0
        assert self.company.price_to_ratios.count() == 0
        assert self.company.ev_ratios.count() == 0
        assert self.company.efficiency_ratios.count() == 0
        assert self.company.growth_rates.count() == 0

        created_current_stock_price = self.company_update.create_current_stock_price(
            price=current_data["currentPrice"]
        )
        created_rentability_ratios = self.company_update.create_rentability_ratios(
            rentability_ratios
        )
        created_liquidity_ratio = self.company_update.create_liquidity_ratio(liquidity_ratio)
        created_margin_ratio = self.company_update.create_margin_ratio(margin_ratio)
        created_fcf_ratio = self.company_update.create_fcf_ratio(fcf_ratio)
        created_ps_value = self.company_update.create_ps_value(ps_value)
        created_non_gaap = self.company_update.create_non_gaap(non_gaap)
        created_operation_risk_ratio = self.company_update.create_operation_risk_ratio(
            operation_risk_ratio
        )
        created_price_to_ratio = self.company_update.create_price_to_ratio(price_to_ratio)
        created_enterprise_value_ratio = self.company_update.create_enterprise_value_ratio(
            enterprise_value_ratio
        )
        created_eficiency_ratio = self.company_update.create_eficiency_ratio(eficiency_ratio)
        created_company_growth = self.company_update.create_company_growth(company_growth)

        assert created_current_stock_price.price == current_data["currentPrice"]

        assert self.company.stock_prices.latest().price == current_data["currentPrice"]
        assert self.company.rentability_ratios.latest() == created_rentability_ratios
        assert self.company.liquidity_ratios.latest() == created_liquidity_ratio
        assert self.company.margins.latest() == created_margin_ratio
        assert self.company.fcf_ratios.latest() == created_fcf_ratio
        assert self.company.per_share_values.latest() == created_ps_value
        assert self.company.non_gaap_figures.latest() == created_non_gaap
        assert self.company.operation_risks_ratios.latest() == created_operation_risk_ratio
        assert self.company.price_to_ratios.latest() == created_price_to_ratio
        assert self.company.ev_ratios.latest() == created_enterprise_value_ratio
        assert self.company.efficiency_ratios.latest() == created_eficiency_ratio
        assert self.company.growth_rates.latest() == created_company_growth

        assert self.company.stock_prices.count() == 1
        assert self.company.rentability_ratios.count() == 1
        assert self.company.liquidity_ratios.count() == 1
        assert self.company.margins.count() == 1
        assert self.company.fcf_ratios.count() == 1
        assert self.company.per_share_values.count() == 1
        assert self.company.non_gaap_figures.count() == 1
        assert self.company.operation_risks_ratios.count() == 1
        assert self.company.price_to_ratios.count() == 1
        assert self.company.ev_ratios.count() == 1
        assert self.company.efficiency_ratios.count() == 1
        assert self.company.growth_rates.count() == 1

    def test_requests(self):
        up_comp = UpdateCompany(self.zinga)
        up_comp.request_income_statements_finprep()
        time.sleep(5)
        up_comp.request_balance_sheets_finprep()
        time.sleep(5)
        up_comp.request_cashflow_statements_finprep()
