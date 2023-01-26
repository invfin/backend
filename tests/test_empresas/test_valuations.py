from src.empresas.outils.valuations import discounted_cashflow, graham_value, margin_of_safety


class TestValuation:
    def test_discounted_cashflow(self):
        assert 11.29 == discounted_cashflow(
            last_revenue=6464164,
            revenue_growth=13,
            net_income_margin=10.2,
            fcf_margin=22.5,
            buyback=5,
            average_shares_out=545678,
        )

    def test_graham_value(self):
        assert 9.19 == graham_value(2.5, 1.5)

    def test_margin_of_safety(self):
        assert 57.0 == margin_of_safety(23, 10)
