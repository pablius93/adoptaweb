from django.contrib import admin
from .models import *

admin.autodiscover()


class ApiKeysAdmin(admin.ModelAdmin):
    list_display = ('user', 'key',)

admin.site.register(ApiKeys, ApiKeysAdmin)
