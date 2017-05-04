from test_plus.test import TestCase
from .models import *


class TestPetModels(TestCase):

    def setUp(self):
        self.names = ['Duna', 'Zero', 'Roland', 'Nirvana', 'Lua', 'Sparky']
        self.expected_slug = ['duna', 'zero', 'roland', 'nirvana', 'lua', 'sparky']
        self.days_waiting = 6
        self.user = self.make_user()

    def test_create_pets(self):
        for i in range(0, len(self.names)):
            pet = Pet()
            pet.name = self.names[i]
            pet.owner = self.user
            pet.save()
            self.assertEqual(pet.slug, self.expected_slug[i])  # slug correct
        count = Pet.objects.count()
        self.assertEqual(count, len(self.names))  # correct number of pets created

    def test_pet_days_waiting(self):
        pet = Pet()
        pet.name = self.names[0]
        pet.since = datetime.datetime.now() - datetime.timedelta(days=self.days_waiting)
        self.assertEqual(pet.get_days_waiting(), self.days_waiting)
