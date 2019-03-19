from django.test import TestCase, Client, SimpleTestCase
import unittest


# Create your tests here.

class IndexPage(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_is_up(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
