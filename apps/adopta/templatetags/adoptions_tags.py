from django import template
from apps.adopta.models import *
from config.settings.base import MEDIA_URL

register = template.Library()


@register.simple_tag()
def get_days_waiting(pet):
    return (datetime.datetime.now().date() - pet.since.date()).days


@register.simple_tag()
def get_first_image(pet):
    image = ''
    try:
        image = PetImage.objects.filter(pet=pet)[0].image
    except IndexError:
        print('No Pet Images created')
    return image


@register.simple_tag()
def get_thumbnail_image(pet):
    image = ''
    try:
        image = PetImage.objects.filter(pet=pet)[0].thumbnail
    except IndexError:
        print('No Pet Images created')
    return '{}{}'.format(MEDIA_URL, image)


@register.simple_tag
def request_exists(pet, user):
    exists = False
    try:
        chats = AdoptionChat.objects.get(request_user=user, pet=pet, adoption_user=pet.owner)
        exists = True
    except:
        exists = False
    return exists
