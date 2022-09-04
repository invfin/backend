from typing import Union, Tuple

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps
from django.conf import settings

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog

from apps.seo.outils.visiteur_meta import SeoInformation
from apps.seo.models import (
    UserJourney,
    Visiteur,
    VisiteurJourney,
)


User = get_user_model()


class JourneyClassifier:
    def get_user_or_visiteur(
        self,
        request
    ) -> Tuple[Union[Visiteur, User], str, Union[VisiteurJourney, UserJourney]]:
        if request.user.is_authenticated:
            default_journey_model = UserJourney
            user_str = "User"
            user = request.user

        elif request.user.is_anonymous:
            visiteur = None
            if request.is_visiteur:
                visiteur = request.visiteur
            if not visiteur:
                visiteur = SeoInformation().find_visiteur(request)
            default_journey_model = VisiteurJourney
            user_str = "Visiteur"
            user = visiteur

        return user, user_str, default_journey_model

    def save_journey(self, request, current_path, comes_from):
        user, user_str, default_journey_model = self.get_user_or_visiteur(request)
        journey = default_journey_model.objects.create(
            user=user,
            current_path=current_path,
            comes_from=comes_from,
            parsed = True
        )
        model_visited, journey_model = self.get_specific_journey(current_path)
        if model_visited and journey_model:
            apps.get_model(
                app_label='seo',
                model_name=f'{user_str}{journey_model}'
            ).objects.create(
                user=user,
                visit=journey,
                model_visited=model_visited,
                date=timezone.now()
            )

    def get_specific_journey(
        self,
        current_path
    ) -> Tuple[Union[Company, Term, Question, PublicBlog], str]:
        splited_path = current_path.split('/')

        model_visited, journey_model = None, None

        if len(splited_path) > 3 and not settings.ADMIN_URL in current_path:

            splited_path = splited_path[-3:-1]
            if splited_path[1].startswith('?utm'):
                info = splited_path[0]
            else:
                info = splited_path[1]



            if '/screener/analisis-de/' in current_path:
                journey_model = 'CompanyVisited'
                model_visited = Company.objects.get(ticker=info)

            elif '/p/' in current_path:
                journey_model = 'PublicBlogVisited'
                model_visited = PublicBlog.objects.get(slug=info)

            elif '/question/' in current_path:
                journey_model = 'QuestionVisited'
                model_visited = Question.objects.get(slug=info)

            elif '/definicion/' in current_path:
                journey_model = 'TermVisited'
                model_visited = Term.objects.get(slug=info)

        return model_visited, journey_model


