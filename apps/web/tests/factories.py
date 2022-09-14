from bfet import DjangoTestingModel as DTM
from apps.web.constants import CONTENT_PURPOSES
from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailsType,
    WebsiteEmailTrack,
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign,
)

def generate_web_models():
    for purpose in CONTENT_PURPOSES:
        DTM.create()
