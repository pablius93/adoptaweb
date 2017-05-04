import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone as tz
from django.utils.text import slugify
import datetime
import os
from PIL import Image
from .settings import IMAGE_MAX_SIZE, IMAGE_THUMBNAIL_SIZE
from .utils.uploads import get_image_filename, get_thumbnail_filename


class PetType(models.Model):
    name = models.CharField(max_length=80, verbose_name=_('name'))
    description = models.CharField(max_length=600, verbose_name=_('description'),
                                   null=True, blank=True)
    slug = models.SlugField(max_length=160, verbose_name=_('slug'))

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            urlize = '{}'.format(self.name)
            self.slug = slugify(urlize)
        super(PetType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('pet type')


class Logo(models.Model):
    image = models.ImageField(upload_to=get_image_filename, verbose_name=_('image'))
    thumbnail = models.ImageField(upload_to=get_thumbnail_filename, verbose_name=_('thumbnail'), blank=True)
    is_cover = models.BooleanField(default=False, verbose_name=_('is cover'))

    def save(self, *args, **kwargs):
        if not self.id and not self.image:
            return

        super(Logo, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        factor = 1
        if (width > IMAGE_MAX_SIZE) or (height > IMAGE_MAX_SIZE):
            if width > height:
                factor = width / IMAGE_MAX_SIZE
            else:
                factor = height / IMAGE_MAX_SIZE

        size = (int(width / factor), int(height / factor))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

        if self.is_cover:
            thumbnail = image.resize((IMAGE_THUMBNAIL_SIZE, IMAGE_THUMBNAIL_SIZE), Image.ANTIALIAS)
            thumbnail.save(self.thumbnail.path)

    def delete(self, *args, **kwargs):
        print(self.image.path)
        print(self.thumbnail.path)
        os.remove(self.image.path)
        os.remove(self.thumbnail.path)
        super(Logo, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('logo')


class UserInfo(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    complete_name = models.CharField(max_length=100, verbose_name=_('complete name'))
    phone_number = models.CharField(max_length=12, verbose_name=_('phone number'))
    address = models.CharField(max_length=140, verbose_name=_('address'))
    city = models.CharField(max_length=50, verbose_name=_('city'))
    country = models.CharField(max_length=50, verbose_name=_('country'))

    def __str__(self):
        return '{}: - {}'.format(self.complete_name, self.phone_number)

    def __unicode__(self):
        return '{}: - {}'.format(self.complete_name, self.phone_number)


class Organisation(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    name = models.CharField(max_length=100, verbose_name=_('complete name'))
    phone_number = models.CharField(max_length=12, verbose_name=_('phone number'))
    address = models.CharField(max_length=140, verbose_name=_('address'))
    city = models.CharField(max_length=50, verbose_name=_('city'))
    country = models.CharField(max_length=50, verbose_name=_('country'))
    web = models.CharField(max_length=100, null=True, verbose_name=_('web'))
    email = models.CharField(max_length=100, null=True, verbose_name=_('email'))
    logo = models.OneToOneField(Logo, null=True, on_delete=models.CASCADE, verbose_name=_('logo'))

    def __str__(self):
        return '{}: - {}'.format(self.name, self.phone_number)

    def __unicode__(self):
        return '{}: - {}'.format(self.name, self.phone_number)


class Pet(models.Model):
    """ Pet model """
    name = models.CharField(max_length=80, verbose_name=_('name'))
    owner = models.ForeignKey(User, verbose_name=_('owner'))
    type = models.ForeignKey(PetType, null=True, blank=True, verbose_name=_('type'))
    since = models.DateTimeField(default=tz.now, verbose_name=_('since'))
    description = models.CharField(max_length=1200, verbose_name=_('description'))
    adopted = models.BooleanField(default=False, verbose_name=_('adopted'))
    slug = models.SlugField(max_length=160, verbose_name=_('slug'))

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Pet, self).save(*args, **kwargs)

    def get_days_waiting(self):
        return (datetime.datetime.now().date() - self.since.date()).days

    class Meta:
        verbose_name = _('pet')


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, blank=True, null=True, verbose_name=_('pet'))
    image = models.ImageField(upload_to=get_image_filename, verbose_name=_('image'))
    thumbnail = models.ImageField(upload_to=get_thumbnail_filename, verbose_name=_('thumbnail'), blank=True)
    is_cover = models.BooleanField(default=False, verbose_name=_('is cover'))

    def save(self, *args, **kwargs):
        if not self.id and not self.image:
            return

        super(PetImage, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        factor = 1
        if (width > IMAGE_MAX_SIZE) or (height > IMAGE_MAX_SIZE):
            if width > height:
                factor = width / IMAGE_MAX_SIZE
            else:
                factor = height / IMAGE_MAX_SIZE

        size = (int(width / factor), int(height / factor))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

        if self.is_cover:
            thumbnail = image.resize((IMAGE_THUMBNAIL_SIZE, IMAGE_THUMBNAIL_SIZE), Image.ANTIALIAS)
            thumbnail.save(self.thumbnail.path)

    def delete(self, *args, **kwargs):
        print(self.image.path)
        print(self.thumbnail.path)
        os.remove(self.image.path)
        os.remove(self.thumbnail.path)
        super(PetImage, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('pet image')


class AdoptionRequest(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    pet = models.ForeignKey(Pet, verbose_name=_('pet'))
    date = models.DateTimeField(default=tz.now, verbose_name=_('date'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last name'))
    address = models.CharField(max_length=140, verbose_name=_('address'))
    why = models.TextField(max_length=1200, verbose_name=_('why'))
    read = models.BooleanField(default=False, verbose_name=_('read'))

    class Meta:
        verbose_name = _('adoption request')

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.date, self.why)

    def __unicode__(self):
        return '{}-{}-{}'.format(self.user, self.date, self.why)


class PetUpdateFile(models.Model):
    file = models.FileField(upload_to='uploads/files/%Y/%m/%d', verbose_name=_('file'))

    class Meta:
        verbose_name = _('feedback file')


class PetUpdate(models.Model):
    pet = models.ForeignKey(Pet, verbose_name=_('pet'))
    content = models.CharField(max_length=400, verbose_name=_('content'))
    date = models.DateTimeField(default=tz.now, verbose_name=_('date'))
    file = models.OneToOneField(PetUpdateFile, null=True, blank=True, verbose_name=_('file'))

    class Meta:
        verbose_name = _('pet update')


class AdoptionChat(models.Model):
    pet = models.ForeignKey(Pet, verbose_name=_('pet'))
    adoption_user = models.ForeignKey(User, related_name='adoption_user', verbose_name=_('adoption user'))
    request_user = models.ForeignKey(User, related_name='request_user', verbose_name=_('request user'))
    creation_date = models.DateTimeField(default=tz.now, verbose_name=_('creation date'))
    last_message_date = models.DateTimeField(null=True, verbose_name=_('last message date'))
    salt = models.CharField(null=True, max_length=32, verbose_name=_('salt'))

    class Meta:
        verbose_name = _('adoption chat')

    def save(self, *args, **kwargs):
        if not self.id:
            self.salt = ''\
                .join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        super(AdoptionChat, self).save(*args, **kwargs)

    def __str__(self):
        return 'Chat-{}'.format(self.id)

    def __unicode__(self):
        return 'Chat-{}'.format(self.id)


class Message(models.Model):
    adoption_chat = models.ForeignKey(AdoptionChat, verbose_name=_('adoption chat'), null=True)
    from_user = models.ForeignKey(User, related_name='from_user', verbose_name=_('from user'))
    when = models.DateTimeField(default=tz.now, verbose_name=_('when'))
    content = models.TextField(max_length=500, blank=False, verbose_name=_('content'))
    read = models.BooleanField(default=False, verbose_name=_('read'))
