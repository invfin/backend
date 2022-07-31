from model_bakery import baker

from apps.web.models import (
Promotion,
PromotionCampaign,
WebsiteEmail,
WebsiteEmailTrack,
WebsiteEmailsType,
WebsiteLegalPage,
)


promotion_campaign = baker.make(PromotionCampaign)
promotion = baker.make(
    Promotion, 
    campaign_related=baker.make(PromotionCampaign)
)
website_email_type = baker.make(WebsiteEmailsType)
website_email = baker.make(
    WebsiteEmail, 
    type_related=baker.make(WebsiteEmailsType)
)
website_email_track = baker.make(
    WebsiteEmailTrack, 
    email_related=baker.make(
        WebsiteEmail, 
        type_related=baker.make(WebsiteEmailsType)
    )
)
website_legal_page = baker.make(WebsiteLegalPage)
