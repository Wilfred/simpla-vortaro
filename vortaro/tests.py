from django.test import TestCase
from django.core.urlresolvers import reverse

class IndexTests(TestCase):
    def test_index_renders(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class AboutTests(TestCase):
    def test_about_renders(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
