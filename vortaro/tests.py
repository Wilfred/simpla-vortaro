# -*- coding: utf-8 -*-
from django_test_mixins import HttpCodeTestCase
from django.test import TestCase
from django.core.urlresolvers import reverse

from vortaro.models import Word, Translation, Definition, Variant


class IndexTests(TestCase):
    def test_index_renders(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegacyUrlTests(HttpCodeTestCase):
    def test_vorto_get_parameter(self):
        Word.objects.create(word="saluto")

        response = self.client.get(reverse('index') + "?vorto=saluto")
        self.assertHttpRedirect(response)

    def test_sercxo_get_parameter(self):
        response = self.client.get(reverse('index') + "?serĉo=saluto")
        self.assertHttpRedirect(response)


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


class SearchPageTests(HttpCodeTestCase):
    def assertFindsWord(self, request, word):
        self.assertIn(word, request.context['matching_words'])
    
    def test_search_renders(self):
        response = self.client.get(reverse('search_word') + '?s=saluton')
        self.assertHttpOK(response)

    def test_search_trailing_apostrophe(self):
        word = Word.objects.create(word="saluto")
        Variant.objects.create(word=word, variant="saluto")
        
        response = self.client.get(reverse('search_word') + "?s=salut'")
        self.assertFindsWord(response, word)

    def test_search_term_contains_hyphen(self):
        word = Word.objects.create(word="saluto")
        Variant.objects.create(word=word, variant="saluto")
        
        response = self.client.get(reverse('search_word') + "?s=salut-o")
        self.assertFindsWord(response, word)

    def test_search_term_leading_hyphen(self):
        """We should preserve leading hyphens, since we have words of this form
        in our dictionary.

        """
        word = Word.objects.create(word="-eg")
        Variant.objects.create(word=word, variant="-eg")
        
        response = self.client.get(reverse('search_word') + "?s=-eg")
        self.assertFindsWord(response, word)

    def test_search_term_case_insensitive(self):
        word = Word.objects.create(word="eĥoŝanĝo")
        Variant.objects.create(word=word, variant="eĥoŝanĝo")
        
        response = self.client.get(reverse('search_word') + "?s=EĤOŜANĜO")
        self.assertFindsWord(response, word)

    def test_search_i_feel_lucky(self):
        word = Word.objects.create(word="saluto")
        Variant.objects.create(word=word, variant="salutoj")
        
        response = self.client.get(reverse('search_word') + '?s=salutoj&rekte=yes')
        self.assertHttpRedirect(response)

    def test_search_renders_translations(self):
        word = Word.objects.create(word="saluto")
        definition = Definition.objects.create(definition="foo")
        Translation.objects.create(word=word, definition=definition,
                                   translation="hello", language_code="en")

        response = self.client.get(reverse('search_word') + '?s=hello')
        self.assertHttpOK(response)
