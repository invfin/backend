import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db
from django.contrib.auth import get_user_model

from bfet import DjangoTestingModel as DTM

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog

from apps.seo.models import (
    Visiteur,
    UserJourney,
    VisiteurJourney,
    UserCompanyVisited,
    VisiteurQuestionVisited
)
from apps.seo.outils.save_journey import JourneyClassifier


User = get_user_model()


class MockRequest:
    user = None
    visiteur = None
    is_visiteur = False


class TestJourneyClassifier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = MockRequest
        cls.user = DTM.create(User)
        cls.visiteur = DTM.create(Visiteur)
        cls.company = DTM.create(Company)
        cls.term = DTM.create(
            Term,
            author=cls.user
        )
        cls.question = DTM.create(
            Question,
            author=cls.user
        )
        cls.blog = DTM.create(
            PublicBlog,
            author=cls.user
        )

    def test_get_user_or_visiteur(self):
        self.client.force_login(self.user)
        user_request = self.request
        user_request.user = self.user
        user_classifier = JourneyClassifier().get_user_or_visiteur(user_request)
        self.assertEqual(self.user, user_classifier[0])
        self.assertEqual("User", user_classifier[1])
        self.assertEqual(UserJourney, user_classifier[2])

        visiteur_request = self.request
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        visiteur_classifier = JourneyClassifier().get_user_or_visiteur(user_request)
        self.assertEqual(self.visiteur, visiteur_classifier[0])
        self.assertEqual("Visiteur", visiteur_classifier[1])
        self.assertEqual(VisiteurJourney, visiteur_classifier[2])

    def test_get_specific_journey(self):
        company_path = self.company.get_absolute_url()
        company_journey = JourneyClassifier().get_specific_journey(company_path)
        self.assertEqual("CompanyVisited", company_journey[0])
        self.assertEqual(self.company, company_journey[1])

        blog_path = self.blog.get_absolute_url()
        blog_journey = JourneyClassifier().get_specific_journey(blog_path)
        self.assertEqual("PublicBlogVisited", blog_journey[0])
        self.assertEqual(self.blog, blog_journey[1])

        question_path = self.question.get_absolute_url()
        question_journey = JourneyClassifier().get_specific_journey(question_path)
        self.assertEqual("QuestionVisited", question_journey[0])
        self.assertEqual(self.question, question_journey[1])

        term_path = self.term.get_absolute_url()
        term_journey = JourneyClassifier().get_specific_journey(term_path)
        self.assertEqual("TermVisited", term_journey[0])
        self.assertEqual(self.term, term_journey[1])

        admin_path = "http://example.com:8000/admin/seo/userjourney/"
        admin_journey = JourneyClassifier().get_specific_journey(admin_path)
        self.assertEqual(None, admin_journey[0])
        self.assertEqual(None, admin_journey[1])

    def test_save_journey(self):
        comes_from = None

        company_path = self.company.get_absolute_url()
        self.assertEqual(0, UserJourney.objects.all().count())
        self.assertEqual(0, UserCompanyVisited.objects.all().count())
        self.client.force_login(self.user)
        user_request = self.request
        user_request.user = self.user
        JourneyClassifier().save_journey(user_request, company_path, comes_from)
        self.assertEqual(1, UserJourney.objects.all().count())
        self.assertEqual(1, UserCompanyVisited.objects.all().count())
        company_visited = UserCompanyVisited.objects.all().first()
        self.assertEqual(
            self.company,
            company_visited.model_visited
        )
        self.assertEqual(
            self.user,
            company_visited.user
        )

        question_path = self.question.get_absolute_url()
        self.assertEqual(0, VisiteurJourney.objects.all().count())
        self.assertEqual(0, VisiteurQuestionVisited.objects.all().count())
        visiteur_request = self.request
        visiteur_request.visiteur = self.visiteur
        visiteur_request.is_visiteur = True
        JourneyClassifier().save_journey(visiteur_request, question_path, comes_from)
        self.assertEqual(1, VisiteurJourney.objects.all().count())
        self.assertEqual(1, VisiteurQuestionVisited.objects.all().count())
        question_visited = VisiteurQuestionVisited.objects.all().first()
        self.assertEqual(
            self.question,
            question_visited.model_visited
        )
        self.assertEqual(
            self.visiteur,
            question_visited.user
        )
