import json
from typing import Optional

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(name="get_recommendations")
def get_recommendations(
    model: str,
    num_recs: int = 5,
    product_id: Optional[int] = None,
    user_id: Optional[int] = None,
):
    params = {
        "publicKey": settings.RECSYS_PUBLIC_KEY,
        "entity": model,
        "target": "product",
        "numberRecommendations": num_recs,
        "title": "Estos temas podrían interesarte",
    }

    if product_id:
        params["prodId"] = product_id

    if user_id:
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
