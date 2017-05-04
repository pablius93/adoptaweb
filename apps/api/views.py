from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

from apps.adopta.models import *
from django.core import serializers
import json
from config.settings.base import MEDIA_URL
from apps.adopta.settings import *
from apps.api.models import ApiKeys
from apps.adopta.utils.str_utils import smart_truncate
from apps.adopta.templatetags.adoptions_tags import get_days_waiting


@login_required
def pet(request, pet_id):
    p = Pet.objects.get(id=pet_id)
    json_response = serializers.serialize('json', [p, ])
    return HttpResponse(json_response)


def pets(request):
    pet_list = Pet.objects.all()
    paginator = Paginator(pet_list, OBJECTS_PER_PAGE)
    page = request.GET.get(PAGINATION_PARAMETER_VALUE)
    results = []
    i = 0
    try:
        out_pets = paginator.page(page)
    except PageNotAnInteger:
        out_pets = paginator.page(1)
    except EmptyPage:
        out_pets = []

    for pet_item in out_pets:
        image_set = PetImage.objects.filter(pet=pet_item, is_cover=True)
        images = []
        for img in image_set:
            images.append(
                {
                    'id': img.id,
                    'image': '{0}{1}'.format(MEDIA_URL, img.image.__str__()),
                    'thumbnail': '{0}{1}'.format(MEDIA_URL, img.thumbnail.__str__()),
                    'is_cover': img.is_cover,
                }
            )
        pd = {
            'id': pet_item.id,
            'name': pet_item.name,
            'description': smart_truncate(pet_item.description, 140, '...'),
            'url': '{0}'.format(reverse('main:pet_detail', args=(pet_item.id, pet_item.slug,))),
            'images': images,
            'days_waiting': get_days_waiting(pet_item)
        }
        results.append(pd)
        i += 1
    return HttpResponse(json.dumps(results))


@login_required
def search_pet(request):
    results = []
    try:
        query = request.GET['q']
        api_key = request.GET['key']
        key_object = ApiKeys.objects.get(user=request.user)
        if key_object.key != api_key:
            return HttpResponse(json.dumps(results))

        p = Pet.objects.filter(name__icontains=query).order_by('since')[:5]
        i = 0
        for pet_item in p:
            image_set = PetImage.objects.filter(pet=pet_item)
            images = []
            for img in image_set:
                images.append(
                    {
                        'id': img.id,
                        'image': '{0}{1}'.format(MEDIA_URL, img.image.__str__()),
                        'thumbnail': '{0}{1}'.format(MEDIA_URL, img.thumbnail.__str__()),
                        'is_cover': img.is_cover,
                    }
                )
            pd = {
                'id': pet_item.id,
                'name': pet_item.name,
                'slug': pet_item.slug,
                'images': images
            }
            results.append(pd)
            i += 1
    except ObjectDoesNotExist:
        print('Error: API Key not valid')
    except MultiValueDictKeyError:
        print('Error')
    return HttpResponse(json.dumps(results))


@login_required
def get_image(request):
    query = request.GET['q']
    p = PetImage.objects.filter(pet=query)[:1]
    json_response = serializers.serialize('json', p)
    return HttpResponse(json_response)


@login_required
def create_api_keys(request):
    try:
        api_key = ApiKeys.objects.get(user=request.user)
    except ObjectDoesNotExist:
        print('Creating API keys...')
        api_key = ApiKeys()
        api_key.user = request.user
        api_key.save()
    return HttpResponseRedirect(reverse('main:first_login'))


@login_required
def get_messages(request, chat_id):
    results = []
    try:
        chat = AdoptionChat.objects.get(id=chat_id)
        if chat.adoption_user == request.user or chat.request_user == request.user:
            messages = Message.objects.filter(adoption_chat=chat).order_by('when')[:MAX_MESSAGES]
            for message in messages:
                msg = {
                    'message_id': message.id,
                    'when': '{:%H:%M}'.format(message.when),
                    'content': message.content,
                    'mine': message.from_user == request.user,
                    'read': message.read,
                    'user': message.from_user.username,
                }
                results.append(msg)
    except ObjectDoesNotExist:
        print('Error: API Key not valid')
    except MultiValueDictKeyError:
        print('Error')
    return HttpResponse(json.dumps(results))


@login_required
def post_message(request, chat_id):
    try:
        chat = AdoptionChat.objects.get(id=chat_id)
        content = request.POST['content']
        message = Message()
        message.content = content
        message.adoption_chat = chat
        message.from_user = request.user
        message.save()
        chat.last_message_date = tz.now()
        chat.save()
    except ObjectDoesNotExist:
        print('Error: Chat not found')
        return HttpResponse({'status': 403})
    except:
        print('Error: POST[content] not valid')
        return HttpResponse({'status': 400})
    return HttpResponse({'status': 200})


@login_required
def get_chats(request):
    chats = AdoptionChat.objects.filter(
        Q(adoption_user=request.user) | Q(request_user=request.user)
    ).order_by('last_message_date')
    results = []
    for chat in chats:
        results.append(
            {
                'id': chat.id,
                'adoption_user': chat.adoption_user.username,
                'request_user': chat.request_user.username,
            }
        )
    return HttpResponse(json.dumps(results))


@login_required
def get_chat(request, chat_id):
    chat = AdoptionChat.objects.get(id=chat_id)
    json_response = []
    if chat.request_user == request.user or chat.adoption_user == request.user:
        json_response = serializers.serialize('json', [chat, ])
    return HttpResponse(json_response)


@login_required
def new_pet_update(request, pet_id):
    try:
        p = Pet.objects.get(id=pet_id)
        content = request.POST['content']
        pet_update = PetUpdate()
        pet_update.content = content
        pet_update.pet = p
        pet_update.save()
        print('New Pet Update saved')
    except ObjectDoesNotExist:
        print('Error: Chat not found')
        return HttpResponse({'status': 403})
    except:
        print('Error: POST[content] not valid')
        return HttpResponse({'status': 400})
    return HttpResponse({'status': 200})
