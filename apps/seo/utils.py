
def generate_utm_url(
        utm_source: str,
        utm_medium: str,
        utm_campaign: str,
        utm_term: str,
        link: str = None
    ) -> str:
        utm_source = f'utm_source={utm_source}'
        utm_medium = f'utm_medium={utm_medium}'
        utm_campaign = f'utm_campaign={utm_campaign}'
        utm_term = f'utm_term={utm_term}'
        utm_params = f'{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'
        if link:
            return f'{link}?{utm_params}'
        return utm_params
