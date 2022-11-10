from typing import Union, Tuple, Optional, Type

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
        self, request
    ) -> Tuple[
        Optional[Union[Type[Visiteur], Type[User]]],
        Optional[str],
        Optional[Union[Type[VisiteurJourney], Type[UserJourney]]],
    ]:
        default_journey_model = None
        user_str = ""
        user = None
        if hasattr(request, "auth") and request.auth and request.auth.user == request.user:
            # Come from API endpoint
            pass
        else:
            # Is a "regular user" from a regular view
            if request.user.is_authenticated:
                default_journey_model = UserJourney
                user_str = "User"
                user = request.user

            elif request.user.is_anonymous:
                visiteur = None
                if hasattr(request, "is_visiteur") and request.is_visiteur:
                    visiteur = request.visiteur
                if not visiteur:
                    visiteur = SeoInformation().find_visiteur(request)
                default_journey_model = VisiteurJourney
                user_str = "Visiteur"
                user = visiteur

        return user, user_str, default_journey_model

    def save_journey(self, request, current_path, comes_from):
        user, user_str, default_journey_model = self.get_user_or_visiteur(request)
        if default_journey_model:
            journey = default_journey_model.objects.create(
                user=user, current_path=current_path, comes_from=comes_from, parsed=True
            )
            model_visited, journey_model = self.get_specific_journey(current_path)
            if model_visited and journey_model:
                apps.get_model(app_label="seo", model_name=f"{user_str}{journey_model}").objects.create(
                    user=user, visit=journey, model_visited=model_visited, date=timezone.now()
                )

    def get_specific_journey(
        self, current_path
    ) -> Tuple[Optional[Union[Type[Company], Type[Term], Type[Question], Type[PublicBlog]]], Optional[str]]:
        splited_path = current_path.split("/")

        model_visited, journey_model = None, None

        if all(
            [
                len(splited_path) > 3,
                settings.ADMIN_URL not in current_path,
                "href=/static/" not in current_path,
            ]
        ):
            splited_path = splited_path[-3:-1]
            if splited_path[1].startswith("?utm"):
                info = splited_path[0]
            else:
                info = splited_path[1]

            if "general/assets" in current_path:
                return None, None

            if "/screener/analisis-de/" in current_path:
                journey_model = "CompanyVisited"
                model_visited = Company.objects.get(ticker=info)

            elif "/p/" in current_path:
                journey_model = "PublicBlogVisited"
                model_visited = PublicBlog.objects.get(slug=info)

            elif "/question/" in current_path:
                journey_model = "QuestionVisited"
                model_visited = Question.objects.get(slug=info)

            elif "/definicion/" in current_path:
                journey_model = "TermVisited"
                model_visited = Term.objects.filter(slug=info)
                if model_visited.exists():
                    model_visited = model_visited.first()
                else:
                    model_visited, journey_model = None, None

        return model_visited, journey_model
