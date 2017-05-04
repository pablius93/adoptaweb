"""
Development settings
"""
from config.settings.base import *   # noqa

# Development Apps Installed
DEV_APPS = [
    'corsheaders',
]

INSTALLED_APPS += DEV_APPS

# Development middleware
DEV_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

MIDDLEWARE += DEV_MIDDLEWARE

# Development Email settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DJANGO_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS Allowed
# This allows to access the API in dev environment
CORS_ORIGIN_ALLOW_ALL = True

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES' : [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
