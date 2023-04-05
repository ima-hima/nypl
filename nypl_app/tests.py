import unittest
import mock

from django.test import Client

class Test_views(unittest.TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_status_200(self):
        """
        This would be better if I mocked a json response, rather than making
        a call to the API, but figuring out how to mock json responses in Django
         was beyond the scope of this project.
        """
        response = self.client.get('/', {'query': 'cats'})
        assert(response.status_code == 200)

    def test_bad_query(self):
        response = self.client.get('/', {'q': 'cats'})
        assert(response.status_code == 400)

    def test_missing_query(self):
        response = self.client.get('/')
        assert(response.status_code == 400)

