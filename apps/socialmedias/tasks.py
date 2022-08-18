from config import celery_app

from apps.socialmedias import constants

from .poster import SocialPosting


@celery_app.task()
def socialmedia_share_company():
    SocialPosting().share_content(
        constants.COMPANY,
        [
            {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT}
        ]
    )


@celery_app.task()
def socialmedia_share_news():
    SocialPosting().share_content(
        constants.NEWS,
        [
            {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT}
        ]
    )


@celery_app.task()
def socialmedia_share_term():
    SocialPosting().share_content(
        constants.TERM,
        [
            {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT}
        ]
    )


@celery_app.task()
def socialmedia_share_blog():
    SocialPosting().share_content(
        constants.BLOG,
        [
            {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT_IMAGE},
            {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT_IMAGE}
        ]
    )


@celery_app.task()
def socialmedia_share_question():

    SocialPosting().share_content(
        constants.QUESTION,
        [
            {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT}
        ]
    )
