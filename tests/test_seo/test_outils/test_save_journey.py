import pytest

from django.contrib.auth import get_user_model

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog

from apps.seo.models import Visiteur, UserJourney, VisiteurJourney, UserCompanyVisited, VisiteurQuestionVisited
from apps.seo.outils.save_journey import JourneyClassifier


User = get_user_model()


class MockRequest:
    user = None
    visiteur = None
    is_visiteur = False


@pytest.mark.django_db
class TestJourneyClassifier:
    @classmethod
    def setup_class(cls):
        cls.request = MockRequest
        cls.user = DTM.create(User)
        cls.visiteur = DTM.create(Visiteur)
        cls.company = DTM.create(Company)
        cls.term = DTM.create(Term, author=cls.user)
        cls.question = DTM.create(Question, author=cls.user)
        cls.blog = DTM.create(PublicBlog, author=cls.user)

    def test_get_user_or_visiteur(self):
        self.client.force_login(self.user)
        user_request = self.request
        user_request.user = self.user
        user_classifier = JourneyClassifier().get_user_or_visiteur(user_request)
        assert self.user == user_classifier[0]
        assert "User" == user_classifier[1]
        assert UserJourney == user_classifier[2]

        visiteur_request = self.request
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        visiteur_classifier = JourneyClassifier().get_user_or_visiteur(user_request)
        assert self.visiteur == visiteur_classifier[0]
        assert "Visiteur" == visiteur_classifier[1]
        assert (VisiteurJourney, visiteur_classifier[2])

    def test_get_specific_journey(self):
        company_path = self.company.get_absolute_url()
        company_journey = JourneyClassifier().get_specific_journey(company_path)
        assert "CompanyVisited" == company_journey[0]
        assert self.company == company_journey[1]

        blog_path = self.blog.get_absolute_url()
        blog_journey = JourneyClassifier().get_specific_journey(blog_path)
        assert "PublicBlogVisited" == blog_journey[0]
        assert self.blog == blog_journey[1]

        question_path = self.question.get_absolute_url()
        question_journey = JourneyClassifier().get_specific_journey(question_path)
        assert "QuestionVisited" == question_journey[0]
        assert self.question == question_journey[1]

        term_path = self.term.get_absolute_url()
        term_journey = JourneyClassifier().get_specific_journey(term_path)
        assert "TermVisited" == term_journey[0]
        assert self.term == term_journey[1]

        admin_path = "http://example.com:8000/admin/seo/userjourney/"
        admin_journey = JourneyClassifier().get_specific_journey(admin_path)
        assert not admin_journey[0]
        assert not admin_journey[1]

    def test_save_journey(self):
        comes_from = None
        company_path = self.company.get_absolute_url()
        assert 0 == UserJourney.objects.all().count()
        assert 0 == UserCompanyVisited.objects.all().count()

        self.client.force_login(self.user)
        user_request = self.request
        user_request.user = self.user
        JourneyClassifier().save_journey(user_request, company_path, comes_from)
        assert 1 == UserJourney.objects.all().count()
        assert 1 == UserCompanyVisited.objects.all().count()

        company_visited = UserCompanyVisited.objects.all().first()
        assert self.company == company_visited.model_visited
        assert self.user == company_visited.user

        question_path = self.question.get_absolute_url()
        assert 0 == VisiteurJourney.objects.all().count()
        assert 0 == VisiteurQuestionVisited.objects.all().count()

        visiteur_request = self.request
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        JourneyClassifier().save_journey(visiteur_request, question_path, comes_from)
        assert 1 == VisiteurJourney.objects.all().count()
        assert 1 == VisiteurQuestionVisited.objects.all().count()
        question_visited = VisiteurQuestionVisited.objects.all().first()
        assert self.question == question_visited.model_visited
        assert self.visiteur == question_visited.user
