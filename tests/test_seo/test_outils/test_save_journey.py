from django.contrib.auth import get_user_model
from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import Company
from src.escritos.models import Term
from src.preguntas_respuestas.models import Question
from src.public_blog.models import PublicBlog, WritterProfile
from src.seo.models import UserCompanyVisited, UserJourney, Visiteur, VisiteurJourney, VisiteurQuestionVisited
from src.seo.outils.save_journey import JourneyClassifier

User = get_user_model()


class AnonymousUser:
    is_authenticated = False
    is_anonymous = True


class MockRequest:
    user = AnonymousUser()
    visiteur = None
    is_visiteur = False


class TestJourneyClassifier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = DjangoTestingModel.create(User, is_writter=True)
        DjangoTestingModel.create(WritterProfile, user=cls.user)
        cls.visiteur = DjangoTestingModel.create(Visiteur)
        cls.company = DjangoTestingModel.create(Company, ticker="company")
        cls.term = DjangoTestingModel.create(Term, author=cls.user, slug="term")
        cls.question = DjangoTestingModel.create(Question, author=cls.user, slug="question")
        cls.blog = DjangoTestingModel.create(PublicBlog, author=cls.user, slug="blog")

    def test_get_user_or_visiteur(self):
        visiteur_request = MockRequest()
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        user, user_str, default_journey_model = JourneyClassifier().get_user_or_visiteur(visiteur_request)
        assert self.visiteur == user
        assert "Visiteur" == user_str
        assert VisiteurJourney == default_journey_model

        self.client.force_login(self.user)
        user_request = MockRequest()
        user_request.user = self.user
        user, user_str, default_journey_model = JourneyClassifier().get_user_or_visiteur(user_request)
        assert self.user == user
        assert "User" == user_str
        assert UserJourney == default_journey_model

    def test_get_specific_journey(self):
        for model, model_visited_str in [
            (self.company, "CompanyVisited"),
            (self.blog, "PublicBlogVisited"),
            (self.question, "QuestionVisited"),
            (self.term, "TermVisited"),
        ]:
            with self.subTest(model_visited_str):
                model_path = f"http://example.com:8000{model.get_absolute_url()}"
                model_visited, journey_model = JourneyClassifier().get_specific_journey(model_path)
                assert model_visited_str == journey_model
                assert model == model_visited

        for null_path, path_name in [
            ("http://example.com:8000/admin/seo/userjourney/", "admin path"),
            ("http://example.com:8000/static/image/alguna/", "media path"),
            ("http://example.com:8000/general/assets/alguna/", "general assets path"),
        ]:
            with self.subTest(path_name):
                model_visited, journey_model = JourneyClassifier().get_specific_journey(null_path)
                assert model_visited is None
                assert journey_model is None

    def test_save_journey(self):
        comes_from = None
        company_path = self.company.get_absolute_url()
        assert 0 == UserJourney.objects.all().count()
        assert 0 == UserCompanyVisited.objects.all().count()

        self.client.force_login(self.user)
        user_request = MockRequest()
        user_request.user = self.user
        JourneyClassifier().save_journey(user_request, f"http://example.com:8000{company_path}", comes_from)
        assert 1 == UserJourney.objects.all().count()
        assert 1 == UserCompanyVisited.objects.all().count()

        company_visited = UserCompanyVisited.objects.all().first()
        assert self.company == company_visited.model_visited
        assert self.user == company_visited.user

        question_path = self.question.get_absolute_url()

        assert 0 == VisiteurJourney.objects.all().count()
        assert 0 == VisiteurQuestionVisited.objects.all().count()

        visiteur_request = MockRequest()
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        JourneyClassifier().save_journey(visiteur_request, f"http://example.com:8000{question_path}", comes_from)
        assert 1 == VisiteurJourney.objects.all().count()
        assert 1 == VisiteurQuestionVisited.objects.all().count()
        question_visited = VisiteurQuestionVisited.objects.all().first()
        assert self.question == question_visited.model_visited
        assert self.visiteur == question_visited.user
