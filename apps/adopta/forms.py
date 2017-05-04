from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *
from .settings import MAX_UPLOAD_SIZE


class NewPetForm(forms.Form):
    """
    New Pet form
    """
    name = forms.CharField(
        max_length=Pet._meta.get_field('name').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Nombre de la mascota',
                'id': 'pet-name',
            }
        ),
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(
            {
                'placeholder': 'Añade una descripción',
                'cols': 30,
                'rows': 5,
                'id': 'pet-description',
            }
        ),
        max_length=Pet._meta.get_field('description').max_length,
        required=True
    )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            {
                'multiple': True,
                'max_upload_size': MAX_UPLOAD_SIZE,
                'accept': 'image/*',
                'id': 'pet-image',
            },
        )
    )


class AdoptionRequestForm(forms.Form):
    why = forms.CharField(
        widget=forms.Textarea(
            {
                'id': 'why',
                'placeholder': '¿Por qué quieres adoptarlo?',
                'cols': 30,
                'rows': 10,
            }
        ),
        max_length=AdoptionRequest._meta.get_field('why').max_length,
        required=True,
    )


class SearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        max_length=140,
        widget=forms.TextInput(
            {
                'id': 'search-box',
                'class': 'search-box',
                'placeholder': 'Buscar',
                'autocomplete': 'off',
            }
        )
    )


class NewPetUpdateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            {
                'id': 'update-content',
                'placeholder': 'Escribe aquí las novedades',
                'cols': 30,
                'rows': 5,
            }
        ),
        max_length=PetUpdate._meta.get_field('content').max_length,
        required=True,
    )


class NewOrganisationForm(forms.Form):
    name = forms.CharField(
        max_length=Organisation._meta.get_field('name').max_length,
        widget=forms.TextInput(
            {
                'id': 'assoc-name',
                'placeholder': 'Nombre de la asociación',
            }
        )
    )

    address = forms.CharField(
        max_length=Organisation._meta.get_field('address').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Dirección',
                'id': 'assoc-address',
            }
        ),
        required=True,
    )

    town = forms.CharField(
        max_length=Organisation._meta.get_field('city').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Localidad',
                'id': 'assoc-town',
            }
        ),
        required=True,
    )

    phone_number = forms.CharField(
        max_length=Organisation._meta.get_field('phone_number').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Teléfono de contacto',
                'pattern': '[0-9]{9}',
                'id': 'assoc-phone-number',
            }
        ),
        required=True
    )

    web = forms.CharField(
        max_length=Organisation._meta.get_field('web').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Página web',
                'id': 'assoc-web',
            }
        ),
    )


class UserInfoForm(forms.Form):
    complete_name = forms.CharField(
        max_length=UserInfo._meta.get_field('complete_name').max_length,
        widget=forms.TextInput(
            {
                'id': 'assoc-contact-info-name',
                'placeholder': 'Nombre de la asociación',
            }
        )
    )

    address = forms.CharField(
        max_length=UserInfo._meta.get_field('address').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Dirección',
                'id': 'assoc-address',
            }
        ),
        required=True,
    )

    town = forms.CharField(
        max_length=UserInfo._meta.get_field('city').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Localidad',
                'id': 'assoc-town',
            }
        ),
        required=True,
    )

    phone_number = forms.CharField(
        max_length=UserInfo._meta.get_field('phone_number').max_length,
        widget=forms.TextInput(
            {
                'placeholder': 'Teléfono de contacto',
                'pattern': '[0-9]{9}',
                'id': 'assoc-phone-number',
            }
        ),
        required=True
    )
