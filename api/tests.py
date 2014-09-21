from django.core.urlresolvers import reverse
from django_test_mixins import HttpCodeTestCase

from vortaro.models import Word


class WordApiTest(HttpCodeTestCase):
    def test_get_word(self):
        Word.objects.create(word="saluto")

        response = self.client.get(reverse('api_view_word', args=['saluto']))
        self.assertHttpOK(response)
        self.assertEqual(response['Content-Type'], 'application/json')
