from unittest import skip

from django.contrib.auth import get_user_model
from django.test import RequestFactory

from bfet import DjangoTestingModel
from rest_framework.test import APITestCase

from src.empresas.models import Company

User = get_user_model()


@skip("Need to be better")
class TestInvoicesAllAPI(APITestCase):
    def setUp(self):
        self.user = DjangoTestingModel.create(User)
        self.company = DjangoTestingModel.create(Company)

    @skip("not ready")
    def test_roboadvisor_question_company_analysis_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-analysis"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_financial_situation_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-financial"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_investor_experience_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-experience"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_portfolio_assets_weight_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-weights"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_portfolio_composition_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-composition"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_risk_aversion_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-risk-aversion"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_question_stocks_portfolio_API_view(self, rf: RequestFactory):
        data = {}
        url = "/robo-step-stocks-portfolio"
        rf.post(url, data=data)

    @skip("not ready")
    def test_roboadvisor_result(self):
        slug = ""
        f"/robo-result/{slug}/"
