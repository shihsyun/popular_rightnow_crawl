# Create your tests here.
from django.test import TestCase
import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        # Issue a GET request.
        response = self.client.get('')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response is not 404.
        self.assertNotEqual(response.status_code, 404)

    def test_home_404(self):
        # Issue a GET request.
        response = self.client.get('')

        # Check that the response is not 404.
        self.assertNotEqual(response.status_code, 404)
