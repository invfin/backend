from django.contrib.auth import get_user_model

from config import celery_app

User = get_user_model()


@celery_app.task()
def update_users_last_time_seen():
    for user in User.objects.all():
        try:
            last_journey_date = user.journeys.all().latest().date
            user.last_time_seen = last_journey_date
            user.save(update_fields=['last_time_seen'])
        except:
            continue
