from django.conf import settings

from pyfacebook import GraphAPI

import requests
from django.core.management import BaseCommand

from src.socialmedias import constants
from src.socialmedias.outils.socialposter.facepy import Facebook


class Command(BaseCommand):
    def handle(self, *args, **options):
        # facebook = Facebook(
        #     settings.TEST_FACEBOOK_ID,
        #     settings.TEST_FB_PAGE_ACCESS_TOKEN,
        #     "Inversiones.y.Finanzas.Para.Todos.Tests",
        # )
        settings.FACEBOOK_APP_ID
        settings.FACEBOOK_APP_SECRET
        rediret = "https://inversionesyfinanzas.xyz"
        api = GraphAPI(app_id=settings.FACEBOOK_APP_ID, app_secret=settings.FACEBOOK_APP_SECRET, oauth_flow=True)
        authorization_url, state = api.get_authorization_url(
            redirect_uri=rediret,
            # state="InvFin",
        )
        print(state)
        state = "invfin"

        # s = f"https://www.facebook.com/v15.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={rediret}&state={state}"
        # print(s)
        print(authorization_url)
        # api2 = GraphAPI(app_id=settings.FACEBOOK_APP_ID, app_secret=settings.FACEBOOK_APP_SECRET, oauth_flow=True)
        # response = api2.exchange_user_access_token()
        # # print(response)
        # CODE = "AQDVkz4xXbubatrh8AUZ_Y9KGiIh88xC0IvmU-jdiibjYCMEJjtZzfgwMmoW7T9zWQS8tf_OMHgy9LqD3LEX1iVegvgB66YwHrDXUfD5gD6n7fKQzNnK0NmozFU0FXBnnjjnPeadJ4goFWQ1qSpZQvzcD5y7wqtbBHUR234b66ZhgaTwlD1MkFWcr2UKj0SEhAgYJPQ3MyvDmll2ngjlnwAIJlYgjN-7jQ7-IErLXq3WaAB_8JM6R1l4ZIix-ufD7GN3EfDyfuLE7PFAJo0xJLFxt23oyAFaINidZCOLEP6erM5ru2MZiIsYQ6OMGUfRL50ryr5urYpt7mwyWT3P2xch-Gm3OuNIOcvBbaXvrOodlf-RNL1KHSR9l-mqUbZKmbM"
        # # https://inversionesyfinanzas.xyz/?code=&state=invfin#_=_
        # params = {
        #     "client_id": settings.FACEBOOK_APP_ID,
        #     "redirect_uri": "https://inversionesyfinanzas.xyz/",
        #     "client_secret": settings.FACEBOOK_APP_SECRET,
        #     "code": CODE,
        # }
        # response = requests.get("https://graph.facebook.com/v15.0/oauth/access_token?", params=params)
        # print(response.json())
