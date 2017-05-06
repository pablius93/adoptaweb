from allauth.account.views import LoginForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from apps.adopta import settings
from apps.adopta.forms import *


def index(request):
    if request.user.is_authenticated:
        pet_form = NewPetForm()
        pet_list = Pet.objects.all()
        paginator = Paginator(pet_list, settings.OBJECTS_PER_PAGE)
        page = request.GET.get(settings.PAGINATION_PARAMETER_VALUE)

        try:
            out_pets = paginator.page(page)
            active = int(page)
        except PageNotAnInteger:
            out_pets = paginator.page(1)
            active = 1
        except EmptyPage:
            out_pets = paginator.page(paginator.num_pages)
            active = paginator.num_pages
        return render(
            request,
            'main/index.html',
            {
                'pets': out_pets,
                'active': active,
                'previous': active - 1,
                'next': active + 1,
                'last_page': paginator.num_pages,
                'search_form': SearchForm(),
                'new_pet_form': pet_form,
            }
        )
    else:
        f = LoginForm()
        return render(
            request,
            'main/intro.html',
            {
                'login_form': f
            }
        )


def pets(request):
    pet_list = Pet.objects.all()
    paginator = Paginator(pet_list, settings.OBJECTS_PER_PAGE)
    page = request.GET.get(settings.PAGINATION_PARAMETER_VALUE)

    try:
        out_pets = paginator.page(page)
        active = int(page)
    except PageNotAnInteger:
        out_pets = paginator.page(1)
        active = 1
    except EmptyPage:
        out_pets = paginator.page(paginator.num_pages)
        active = paginator.num_pages
    return render(
        request,
        'main/index.html',
        {
            'pets': out_pets,
            'active': active,
            'previous': active - 1,
            'next': active + 1,
            'last_page': paginator.num_pages,
            'search_form': SearchForm(),
        }
    )


def pet_detail(request, pet_id, slug):
    p = get_object_or_404(Pet, id=pet_id)
    updates = PetUpdate.objects.filter(pet=p)
    pet_form = NewPetForm()
    adoption_request_form = AdoptionRequestForm()
    contact_info = None
    organisation = None
    is_org = False
    try:
        contact_info = UserInfo.objects.get(user=p.owner)
    except ObjectDoesNotExist:
        print('Contact Info does not exist')
    try:
        organisation = Organisation.objects.get(user=p.owner)
        is_org = True
    except ObjectDoesNotExist:
        print('Organisation does not exist')

    if p.slug != slug:
        raise Http404
    return render(
        request,
        'main/pet.html',
        {
            'pet': p,
            'new_pet_form': pet_form,
            'adoption_request_form': adoption_request_form,
            'search_form': SearchForm(),
            'pet_update_form': NewPetUpdateForm(),
            'updates': updates,
            'contact_info': contact_info,
            'organisation': organisation,
            'is_org': is_org,
        }
    )


@login_required
def new_pet(request):
    if request.method == "POST":
        form = NewPetForm(request.POST, request.FILES)
        if form.is_valid():
            p = Pet()
            p.name = form.cleaned_data['name']
            p.description = form.cleaned_data['description']
            p.owner = request.user
            p.save()
            files = request.FILES.getlist('image')
            i = 0
            for f in files:
                image = PetImage()
                image.pet = p
                image.image = f
                if i == 0:
                    image.is_cover = True
                    image.thumbnail = f
                image.save()
                i += 1
            return HttpResponseRedirect(reverse('main:pet_detail', args=(p.id, p.slug,)))
        else:
            print('Se ha producido un error validando el formulario')
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def edit_pet(request, pet_id, slug):
    p = Pet.objects.get(id=pet_id, slug=slug)
    if request.method == 'GET':
        form = NewPetForm()
        form.name = p.name
        form.description = p.description
        form.complete_name = p.contact_info.complete_name
        form.address = p.contact_info.address
        form.city = p.contact_info.city
        form.phone_number = p.contact_info.phone_number
        return render(
            request,
            'main/edit-pet.html',
            {
                'pet': p,
                'edit_pet_form': form,
                'search_form': SearchForm(),
            }
        )
    elif request.method == 'POST':
        form = NewPetForm(request.POST)
        if form.is_valid():
            p.name = form.cleaned_data['name']
            p.description = form.cleaned_data['description']
            p.owner = request.user
            p.contact_info.complete_name = form.cleaned_data['complete_name']
            p.contact_info.address = form.cleaned_data['address']
            p.contact_info.city = form.cleaned_data['town']
            p.contact_info.phone_number = form.cleaned_data['phone_number']
            p.contact_info.save()
            p.save()
            return HttpResponseRedirect(reverse('main:pet_detail', args=(p.id, p.slug,)))
        else:
            print('Se ha producido un error validando el formulario')
            return HttpResponseRedirect(reverse('main:edit_pet', args=(p.id, p.slug,)))
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def delete_pet(request, pet_id, slug):
    p = Pet.objects.get(id=pet_id, slug=slug)
    if p.owner == request.user:
        p.delete()
    else:
        print('Error: You are not allowed to perform this action')
        return HttpResponseRedirect(reverse('main:pet_details', args=(p.id, p.slug,)))
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def new_adoption_request(request, pet_id, slug):
    if request.method == "POST":
        form = AdoptionRequestForm(request.POST)
        pet = Pet.objects.get(id=pet_id, slug=slug)
        if form.is_valid():
            chat = AdoptionChat()
            chat.pet = pet
            chat.request_user = request.user
            chat.adoption_user = pet.owner
            chat.last_message_date = tz.now()
            chat.save()
            message = Message()
            message.adoption_chat = chat
            message.content = form.cleaned_data['why']
            message.from_user = request.user
            message.save()
            return HttpResponseRedirect(reverse('main:pet_detail', args=(pet.id, pet.slug,)))
        else:
            print('Se ha producido un error validando el formulario')
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def messages(request):
    chats = AdoptionChat.objects.filter(
        Q(adoption_user=request.user) | Q(request_user=request.user)
    ).order_by('-last_message_date')
    return render(
        request,
        'main/chat.html',
        {
            'chats': chats,
            'search_form': SearchForm(),
            'new_pet_form': NewPetForm(),
        }
    )


@login_required
def accept_adoption_request(request, ar_id):
    pass


@login_required
def reject_adoption_request(request, ar_id):
    pass


def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = Pet.objects.filter(name__icontains=q).order_by('since')
            paginator = Paginator(results, settings.OBJECTS_PER_PAGE)
            page = request.GET.get(settings.PAGINATION_PARAMETER_VALUE)

            try:
                out_pets = paginator.page(page)
                active = int(page)
            except PageNotAnInteger:
                out_pets = paginator.page(1)
                active = 1
            except EmptyPage:
                out_pets = paginator.page(paginator.num_pages)
                active = paginator.num_pages
            return render(
                request,
                'main/index.html',
                {
                    'pets': out_pets,
                    'active': active,
                    'previous': active - 1,
                    'next': active + 1,
                    'last_page': paginator.num_pages,
                    'search_form': SearchForm(),
                }
            )
        else:
            print('Se ha producido un error procesando el formulario')
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def first_login(request):
    try:
        UserInfo.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('main:index'))
    except ObjectDoesNotExist:
        print('User Info does not exist, check if its an organisation')

    try:
        Organisation.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('main:index'))
    except ObjectDoesNotExist:
        print('Organisation does not exist, lets create new things')

    return render(
        request,
        'main/first-login.html',
        {
            'user_info_form': UserInfoForm(),
            'organisation_form': NewOrganisationForm(),
            'search_form': SearchForm(),
        }
    )


@login_required
def create_user_info(request):
    try:
        UserInfo.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('main:index'))
    except ObjectDoesNotExist:
        print('User Info does not exist, lets create new things')

    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            user_info = UserInfo()
            user_info.user = request.user
            user_info.complete_name = form.cleaned_data['complete_name']
            user_info.address = form.cleaned_data['address']
            user_info.city = form.cleaned_data['town']
            user_info.phone_number = form.cleaned_data['phone_number']
            user_info.save()
            return HttpResponseRedirect(reverse('main:index'))
        else:
            print('Error: se ha producido un error')
    return HttpResponseRedirect(reverse('main:first_login'))


@login_required
def create_organisation(request):
    try:
        Organisation.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('main:index'))
    except ObjectDoesNotExist:
        print('Organisation does not exist')

    if request.method == 'POST':
        form = NewOrganisationForm(request.POST, request.FILES)
        if form.is_valid():
            organisation = Organisation()
            organisation.user = request.user
            organisation.name = form.cleaned_data['name']
            organisation.address = form.cleaned_data['address']
            organisation.city = form.cleaned_data['town']
            organisation.phone_number = form.cleaned_data['phone_number']
            organisation.web = form.cleaned_data['web']
            organisation.email = request.user.email
            organisation.save()
            return HttpResponseRedirect(reverse('main:index'))
        else:
            print('Error: se ha producido un error')
    return HttpResponseRedirect(reverse('main:first_login'))


def organisations(request):
    return HttpResponseRedirect(reverse('main:index'))
    # orgs = Organisation.objects.all()


@login_required
def my_profile(request):
    try:
        info = UserInfo.objects.get(user=request.user)
        return render(
            request,
            'main/my-profile-user.html',
            {
                'info': info,
                'search_form': SearchForm,
            }
        )
    except ObjectDoesNotExist:
        pass

    try:
        org = Organisation.objects.get(user=request.user)
        return render(
            request,
            'main/my-profile-organisation.html',
            {
                'info': org,
                'search_form': SearchForm(),
            }
        )
    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect(reverse('main:first_login'))
