from typing import Dict

from django.contrib.auth import get_user_model
from django.utils import timezone

from config import celery_app
from src.emailing.tasks import send_email_task
from src.public_blog.models import NewsletterFollowers, PublicBlog, PublicBlogAsNewsletter

User = get_user_model()


@celery_app.task()
def check_programmed_blog_posts_task():
    for blog_post in PublicBlog.objects.filter(status=3):
        if blog_post.date_to_publish <= timezone.now():
            return  # publicar los blogs


@celery_app.task()
def send_newsletter_to_followers_task(writer_id: int, newsletter: Dict):
    writer = User.objects.get(id=writer_id)
    for follower in NewsletterFollowers.objects.get(user=writer):
        send_email_task.delay(newsletter, follower.id, "news")
