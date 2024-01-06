response = {
    "success": True,
    "terms": "https://currencylayer.com/terms",
    "privacy": "https://currencylayer.com/privacy",
    "historical": True,
    "date": "2008-02-01",
    "timestamp": 1201910399,
    "source": "USD",
    "quotes": {
        "USDAED": 3.67135,
        "USDALL": 82.184524,
        "USDAMD": 306.810795,
    },
}


def update_response_quotes(base: str) -> dict[str, str | float | dict[str, float]]:
    quotes = {
        "USD": {
            "USDAED": 3.67135,
            "USDALL": 82.184524,
            "USDAMD": 306.810795,
        },
        "AED": {
            "AEDUSD": 0.27237937,
            "AEDALL": 82.184524,
            "AEDAMD": 306.810795,
        },
        "ALL": {
            "ALLAED": 3.67135,
            "ALLUSD": 0.012167741,
            "ALLAMD": 306.810795,
        },
        "AMD": {
            "AMDAED": 3.67135,
            "AMDALL": 82.184524,
            "AMDUSD": 0.003259338,
        },
    }[base]
    return {
        "success": True,
        "terms": "https://currencylayer.com/terms",
        "privacy": "https://currencylayer.com/privacy",
        "historical": True,
        "date": "2008-02-01",
        "timestamp": 1201910399,
        "source": base,
        "quotes": quotes,
    }
