from django.apps import apps

from config import celery_app
from src.seo.outils.save_journey import JourneyClassifier


@celery_app.task()
def post_promotion():
    pass


@celery_app.task()
def clean_journeys(id, user_journey_model):
    journey = apps.get_model(
        app_label="seo", model_name=f"{user_journey_model}Journey"
    ).objects.get(id=id)
    path = journey.current_path
    model_visited, journey_model = JourneyClassifier().get_specific_journey(path)
    apps.get_model(
        app_label="seo", model_name=f"{user_journey_model}{journey_model}"
    ).objects.create(
        user=journey.user, visit=journey, model_visited=model_visited, date=journey.date
    )
    journey.parsed = True
    journey.save(update_fields=["parsed"])


@celery_app.task()
def loop_over_journeys():
    for user_journey_model in ["User", "Visiteur"]:
        model = apps.get_model(app_label="seo", model_name=f"{user_journey_model}Journey")
        journeys_to_parse = model.objects.filter(parsed=False)
        if journeys_to_parse.exists():
            for journey in journeys_to_parse:
                clean_journeys.delay(journey.id, user_journey_model)
