"""
URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from config.settings import base as settings

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Rest URLs
    url(r'^rest-api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_auth.urls', namespace='rest_auth')),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls',
        namespace='rest_auth_registration')),
    url(r'^accounts/', include('allauth.urls')),

    # Your apps
    url(r'^', include('apps.adopta.urls', namespace='main')),
    url(r'^', include('apps.adopta.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
