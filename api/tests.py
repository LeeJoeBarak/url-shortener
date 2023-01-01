from django.test import TestCase
from django.urls import reverse
import json

from api.models import ShortURL


class URLShortenerTestCase(TestCase):
    def test_create(self):
        # Test creating a new short URL
        url = 'https://ravkavonline.co.il'
        response = self.client.post(reverse('create'), {'url': url}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('short_url', data)
        short_url = data['short_url']

        # Test creating a short URL with an invalid request method
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 400)

        # Test creating a short URL with a missing required field
        response = self.client.post(reverse('create'), {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_redirect(self):
        BASE_URL = "http://localhost:8000/"
        # Test redirecting to a valid short URL
        # short_url = 'http://localhost:8000/abcdefgh'
        short_url = 'abcdefgh'
        ShortURL.objects.create(url='https://ravkavonline.co.il', short_url=short_url)

        response = self.client.get(BASE_URL + short_url)
        self.assertRedirects(response, 'https://ravkavonline.co.il', status_code=302, fetch_redirect_response=False)

        # Test redirecting to a non-existing short URL
        response = self.client.get('http://localhost:8000/invalid')
        self.assertEqual(response.status_code, 404)