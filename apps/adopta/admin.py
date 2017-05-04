from django.contrib import admin
from .models import *

admin.autodiscover()


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'since')


class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class PetImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'pet')


class PetUpdateAdmin(admin.ModelAdmin):
    list_display = ('pet', 'content', 'date')


class FeedbackFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')


class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'user', 'name', 'last_name', 'date', )


class AdoptionChatAdmin(admin.ModelAdmin):
    list_display = ('pet', 'adoption_user', 'request_user',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('adoption_chat', 'content', 'from_user', 'when',)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('complete_name', 'phone_number', 'address', 'city',)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address', 'city', 'web', 'email')

admin.site.register(Pet, PetAdmin)
admin.site.register(PetType, PetTypeAdmin)
admin.site.register(PetImage, PetImageAdmin)
admin.site.register(PetUpdate, PetUpdateAdmin)
admin.site.register(PetUpdateFile, FeedbackFileAdmin)
admin.site.register(AdoptionRequest, AdoptionRequestAdmin)
admin.site.register(AdoptionChat, AdoptionChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Organisation, OrganisationAdmin)
