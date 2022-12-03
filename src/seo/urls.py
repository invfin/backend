from django.urls import path

from src.seo.views import PromotionRedirectView, UrlShorterRedirectView, redirect_old_urls, robots_txt

app_name = "seo"
urlpatterns = [
    path("question/<ques_slug>/", redirect_old_urls, name="question_redirect"),
    path("definicion/<term_slug>/", redirect_old_urls, name="terms_redirect"),
    path("publicaciones/<publs_slug>/", redirect_old_urls, name="publs_redirect"),
    path("aprovecha-la-promocion/<promo_id>/", PromotionRedirectView.as_view(), name="promotion_redirect"),
    # path("aprovecha-la-promocion/<promo_id>/", UrlShorterRedirectView.as_view(), name="url_shorter_redirect"),
    path("robots.txt", robots_txt),
]
