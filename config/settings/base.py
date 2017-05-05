"""
Django settings.
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.__name__)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Environment Variables file
env = environ.Env()

if DEBUG:
    env.read_env(os.path.join(BASE_DIR, '.env.dev'))
else:
    env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='THIS_HAS_TO_BE_SECRET_:)')

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # django-rest-framework
    # See: http://www.django-rest-framework.org/#tutorial
    'rest_framework',
    'rest_framework.authtoken',

    # django-rest-auth
    # See: http://django-rest-auth.readthedocs.io/
    'rest_auth.registration',
]

SOCIAL_APPS = [
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
]

LOCAL_APPS = [
    # Your apps:
    'apps.adopta',
    'apps.api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SOCIAL_ENABLED = env('SOCIAL_ENABLED', default=False)

if SOCIAL_ENABLED == True:
    INSTALLED_APPS += SOCIAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'apps', 'adopta', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.adopta.utils.context_processors.settings_values',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='db'),
        'USER': env('DB_USER', default='user'),
        'PASSWORD': env('DB_PASSWORD', default='password'),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', default=True)

LOGIN_REDIRECT_URL = 'api:create_api_keys'
LOGIN_URL = 'account_login'

SITE_NAME = 'AdoptaWeb'

COPYRIGHT = '&copy; Pablo Moreno, 2017'
MEDIA_URL = '/media/'
GOOGLE_MAPS_API_KEY = ''
META_DESCRIPTION = 'Página web de adopciones de animales abandonados'
META_AUTHOR = 'Pablo Moreno'
META_THEME_COLOR= '#06473D'
