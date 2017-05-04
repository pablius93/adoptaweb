from test_plus.test import TestCase
from django.core.urlresolvers import reverse, resolve
from ..models import *


class TestUrls(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.pet = Pet()
        self.pet.name = 'Duna'
        self.pet.owner = self.user
        self.pet.save()

    def test_index(self):
        self.assertEqual(reverse('main:index'), '/')

    def test_pets(self):
        self.assertEqual(reverse('main:pets'), '/mascotas/')

    def test_pet(self):
        self.assertEqual(
            reverse('main:pet_detail',
                    args=(
                        self.pet.id,
                        self.pet.slug,
                    )),
            '/mascotas/{}/{}/'.format(self.pet.id, self.pet.slug))

    def test_new_pet(self):
        self.assertEqual(reverse('main:new_pet'), '/mascotas/nueva/')
