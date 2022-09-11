from .outils.save_journey import JourneyClassifier

def journey(request):
    current_path = request.build_absolute_uri()
    comes_from = str(request.META.get('HTTP_REFERER'))
    JourneyClassifier().save_journey(request, current_path, comes_from)
    return {}
