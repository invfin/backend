import json

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.simple_tag(name="get_recommendations")
def get_recommendations(model: str, product_id: int = 0, user_id: int = 0):
    params = {
        "publicKey": settings.RECSYS_PUBLIC_KEY,
        "entity": model,
        "target": "product",
        "numberRecommendations": 5,
        "title": "This is a test title",
    }

    if product_id != 0:
        params["prodId"] = product_id

    if user_id != 0:
        params["userId"] = user_id

    endpoint = {
        True: "https://api.elerem.com/assets/embed-widget.js",
        False: "http://localhost:8080/assets/test-embed-widget.js",
    }[settings.IS_PROD]

    return mark_safe(
        "<!-- Elerem Widget BEGIN -->"
        '<div class="elerem-widget-container">'
        '<div class="elerem-widget-container__widget"></div>'
        f'<script type="text/javascript" src="{endpoint}" async>'
        + json.dumps(params, indent=4)
        + "</script></div><!-- Elerem Widget END -->"
    )
