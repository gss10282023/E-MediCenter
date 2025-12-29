from django.conf import settings


def public_config(request):
    google_maps_api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    return {
        "GOOGLE_MAPS_API_KEY": google_maps_api_key,
        "GOOGLE_MAPS_ENABLED": bool(google_maps_api_key),
    }

