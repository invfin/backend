from django.template.defaultfilters import slugify


def generate_url_with_utm(
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_term: str,
    slugify_term: bool = True,
    link: str = "",
) -> str:
    utm_source = f"utm_source={utm_source}"
    utm_medium = f"utm_medium={utm_medium}"
    utm_campaign = f"utm_campaign={utm_campaign}"
    if slugify_term:
        utm_term = slugify(utm_term)
    utm_term = f"utm_term={utm_term}"
    utm_params = f"{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}"
    if link:
        return f"{link}?{utm_params}"
    return utm_params
