from django.test import TestCase
from .qr import generate_qr
import os


class TestQR(TestCase):
    """
    QR Testing class
    """
    def setUp(self):
        self.url = 'https://google.com'
        self.path = '/tmp/google.png'

    def test_create_qr(self):
        """ Creates a new QR Code file and checks whether is created correctly or not"""
        generate_qr(self.url, self.path)
        exists = os.path.isfile(self.path)
        self.assertEqual(exists, True)
        os.remove(self.path)
