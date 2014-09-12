from django_test_mixins import HttpCodeTestCase
from django.test import TestCase
from django.core.urlresolvers import reverse

from vortaro.models import Word


class IndexTests(TestCase):
    def test_index_renders(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class AboutTests(TestCase):
    def test_about_renders(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)


class WordPageTests(HttpCodeTestCase):
    def test_view_renders(self):
        Word.objects.create(word="saluto")
        
        response = self.client.get(reverse('view_word', args=['saluto']))
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_nonexistent_word(self):
        response = self.client.get(reverse('view_word', args=['no_such_word']))
        self.assertHttpRedirect(response)
