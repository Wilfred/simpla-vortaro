from django.core.urlresolvers import reverse
from django_test_mixins import HttpCodeTestCase

import json

from vortaro.models import Word


class WordApiTest(HttpCodeTestCase):
    def test_get_word(self):
        """Ensure that we can call our JSON API and get a response."""
        Word.objects.create(word="saluto")

        response = self.client.get(reverse('api_view_word', args=['saluto']))
        self.assertHttpOK(response)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_word_has_fields(self):
        """Ensure that response from our API have the right fields."""
        Word.objects.create(word="saluto")

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        self.assertIn("vorto", response)
        self.assertIn("difinoj", response)
