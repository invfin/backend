from celery import shared_task

from apps.socialmedias import constants

from .outils.poster import SocialPosting


@shared_task(autoretry_for=(Exception,), max_retries=3)
def socialmedia_share_company():
    SocialPosting().share_content(
        constants.COMPANY,
        [
            {"platform": constants.FACEBOOK},
            {"platform": constants.TWITTER},
        ],
    )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def socialmedia_share_news():
    SocialPosting().share_content(
        constants.NEWS,
        [
            {"platform": constants.FACEBOOK},
            {"platform": constants.TWITTER},
        ],
    )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def socialmedia_share_term():
    SocialPosting().share_content(
        constants.TERM,
        [
            {"platform": constants.FACEBOOK},
            {"platform": constants.TWITTER},
        ],
    )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def socialmedia_share_blog():
    SocialPosting().share_content(
        constants.PUBLIC_BLOG,
        [
            {"platform": constants.FACEBOOK},
            {"platform": constants.TWITTER},
        ],
    )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def socialmedia_share_question():
    SocialPosting().share_content(
        constants.QUESTION,
        [
            {"platform": constants.FACEBOOK},
            {"platform": constants.TWITTER},
        ],
    )
