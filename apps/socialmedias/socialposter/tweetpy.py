import math
import textwrap

import tweepy

from apps.socialmedias import constants


class Twitter:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def do_authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        twitter_api = tweepy.API(auth)
        return twitter_api

    def tweet_text(self, status):
        twitter_api = self.do_authenticate()
        response = twitter_api.update_status(status)
        json_response = response._json
        return json_response["id"]

    def tweet_with_media(self, media_url, status):
        twitter_api = self.do_authenticate()
        post_id = twitter_api.media_upload(media_url)
        response = twitter_api.update_status(status=status, media_ids=[post_id.media_id_string])
        json_response = response._json
        return json_response["id"]

    def create_thread(self, title, link, description, hashtags):
        twitter_api = self.do_authenticate()
        total_number_parts = int(math.ceil(len(description) / constants.TWEET_MAX_LENGTH))

        initial_tweet = f"{title} Más en {link} {hashtags} [0/{total_number_parts}]"
        initial_tweet_response = twitter_api.update_status(initial_tweet)
        list_tweets = [
            {
                "post_type": constants.POST_TYPE_THREAD,
                "social_id": initial_tweet_response.id,
                "description": initial_tweet,
                "platform_shared": constants.TWITTER,
            }
        ]
        for index, part in enumerate(textwrap.wrap(description, constants.TWEET_MAX_LENGTH)):
            if index == 0:
                response = initial_tweet_response
            index += 1
            tweet = f"{part} [{index}/{total_number_parts}]"
            response = twitter_api.update_status(
                status=tweet, in_reply_to_status_id=response.id, auto_populate_reply_metadata=True
            )
            list_tweets.append(
                {
                    "post_type": constants.POST_TYPE_THREAD,
                    "social_id": response.id,
                    "description": tweet,
                    "platform_shared": constants.TWITTER,
                }
            )

        return list_tweets

    def tweet(
        self,
        description: str,
        post_type: int = constants.POST_TYPE_TEXT,
        post_content_type: int = constants.POST_TYPE_TEXT,
        media_url: str = None,
        link: str = None,
        title: str = None,
        **kwargs,
    ):
        if post_content_type == algo:
            post_response = self.create_thread(title, link, description, hashtags)
        elif post_typee = algo_otro:
            pass

            if post_type == constants.POST_TYPE_TEXT or post_type == constants.POST_TYPE_REPOST:
                post_response = self.tweet_text(tweet)

            elif post_type == constants.POST_TYPE_VIDEO or post_type == constants.POST_TYPE_TEXT_VIDEO:
                content_type = "video"

            elif post_type == constants.POST_TYPE_IMAGE or post_type == constants.POST_TYPE_TEXT_IMAGE:
                content_type = "image"

                post_response = self.tweet_with_media(media_url, description)
            

        # Create the posibility of returning a list with all the posts in case of a thread
        if type(post_response) == list:
            twitter_post = {"multiple_posts": True, "posts": post_response}
        else:
            twitter_post = {
                "post_type": post_type,
                "social_id": post_response,
                "description": description,
                "platform_shared": constants.TWITTER,
            }

        return twitter_post
