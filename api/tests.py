from django.core.urlresolvers import reverse
from django_test_mixins import HttpCodeTestCase

import json

from vortaro.models import Word, PrimaryDefinition, Example


class WordApiTest(HttpCodeTestCase):
    def test_get_word(self):
        """Ensure that we can call our JSON API and get a response."""
        Word.objects.create(word="saluto")

        response = self.client.get(reverse('api_view_word', args=['saluto']))
        self.assertHttpOK(response)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_word_404(self):
        response = self.client.get(reverse('api_view_word', args=['no-such-word']))
        self.assertHttpNotFound(response)

    def test_get_word_has_fields(self):
        """Ensure that responses from our API have the right fields."""
        word = Word.objects.create(word="saluto")
        definition = PrimaryDefinition.objects.create(word=word, definition="foo bar")
        Example.objects.create(definition=definition, example="bar baz")

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        self.assertIn("vorto", response)
        self.assertIn("difinoj", response)

        definition_json = response['difinoj'][0]
        self.assertIn("difino", definition_json)
        self.assertIn("pludifinoj", definition_json)
        self.assertIn("ekzemploj", definition_json)

        example_json = definition_json['ekzemploj'][0]
        self.assertIn("ekzemplo", example_json)
        self.assertIn("fonto", example_json)
        
