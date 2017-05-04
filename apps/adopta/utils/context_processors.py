from config.settings import base as settings
from apps.api.models import ApiKeys


def settings_values(request):
    api_key = ''
    try:
        api_key = ApiKeys.objects.get(user=request.user).key
    except:
        print('API key does not exist')
    return {
        'SITE_NAME': settings.SITE_NAME,
        'COPYRIGHT': settings.COPYRIGHT,
        'MEDIA_URL': settings.MEDIA_URL,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'META_THEME_COLOR': settings.META_THEME_COLOR,
        'META_DESCRIPTION': settings.META_DESCRIPTION,
        'META_AUTHOR': settings.META_AUTHOR,
        'API_KEY': api_key,
    }
