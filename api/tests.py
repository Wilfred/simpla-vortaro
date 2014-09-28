# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django_test_mixins import HttpCodeTestCase

import json

from vortaro.models import (
    Word, PrimaryDefinition, Example,
    Translation, Variant, Morpheme)

from initialise_database import get_variants


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

    def test_get_word_has_top_level_fields(self):
        """Ensure that responses from our API have the right fields."""
        Word.objects.create(word="saluto")

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        self.assertIn("vorto", response)
        self.assertIn("difinoj", response)

    def test_get_word_has_definitions(self):
        word = Word.objects.create(word="saluto")
        PrimaryDefinition.objects.create(word=word, definition="foo bar")

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        definition_json = response['difinoj'][0]
        self.assertIn("difino", definition_json)
        self.assertIn("pludifinoj", definition_json)
        self.assertIn("ekzemploj", definition_json)
        self.assertIn("tradukoj", definition_json)

    def test_get_word_has_examples(self):
        word = Word.objects.create(word="saluto")
        definition = PrimaryDefinition.objects.create(word=word, definition="foo bar")
        Example.objects.create(definition=definition, example="bar baz")

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        definition_json = response['difinoj'][0]
        example_json = definition_json['ekzemploj'][0]
        self.assertIn("ekzemplo", example_json)
        self.assertIn("fonto", example_json)

    def test_get_word_has_translations(self):
        word = Word.objects.create(word="saluto")
        definition = PrimaryDefinition.objects.create(word=word, definition="foo bar")
        Translation.objects.create(definition=definition, translation="foo",
                                   language_code='en', word=word)

        raw_response = self.client.get(reverse('api_view_word', args=['saluto']))
        response = json.loads(raw_response.content)

        definition_json = response['difinoj'][0]
        translation_json = definition_json['tradukoj'][0]
        self.assertIn("traduko", translation_json)
        self.assertIn("kodo", translation_json)
        self.assertIn("lingvo", translation_json)


class SearchApiTest(HttpCodeTestCase):
    def test_search(self):
        """Ensure that we can call our JSON API and get a response."""
        response = self.client.get(reverse('api_search_word', args=['saluto']))
        self.assertHttpOK(response)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_search_precise_results(self):
        word_obj = Word.objects.create(word="saluto")
        Variant.objects.create(word=word_obj, variant="saluto")

        raw_response = self.client.get(reverse('api_search_word', args=['saluto']))
        response = json.loads(raw_response.content)

        self.assertEqual(response['preciza'], ['saluto'])

    def test_search_precise_apostrophe(self):
        word_obj = Word.objects.create(word="saluto")
        Variant.objects.create(word=word_obj, variant="saluto")

        raw_response = self.client.get(reverse('api_search_word', args=["salut'"]))
        response = json.loads(raw_response.content)

        self.assertEqual(response['preciza'], ['saluto'])

    def test_search_precise_dash(self):
        word_obj = Word.objects.create(word="saluto")
        Variant.objects.create(word=word_obj, variant="saluto")

        raw_response = self.client.get(reverse('api_search_word', args=["salut-o"]))
        response = json.loads(raw_response.content)

        self.assertEqual(response['preciza'], ['saluto'])

    def test_search_precise_case_insensitive(self):
        word_obj = Word.objects.create(word="saluto")
        Variant.objects.create(word=word_obj, variant="saluto")

        raw_response = self.client.get(reverse('api_search_word', args=["SaLuTo"]))
        response = json.loads(raw_response.content)

        self.assertEqual(response['preciza'], ['saluto'])

    def test_search_precise_results_returns_canonical_noun_form(self):
        word_obj = Word.objects.create(word="hundo")
        for variant in get_variants('hundo'):
            Variant.objects.create(word=word_obj, variant=variant)

        raw_response = self.client.get(reverse('api_search_word', args=['hundojn']))
        response = json.loads(raw_response.content)

        self.assertEqual(response['preciza'], ['hundo'])

    def test_search_precise_results_returns_canonical_adjective_form(self):
        word_obj = Word.objects.create(word="bona")
        for variant in get_variants('bona'):
            Variant.objects.create(word=word_obj, variant=variant)

        raw_response = self.client.get(reverse('api_search_word', args=['bonan']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['bona'])

        raw_response = self.client.get(reverse('api_search_word', args=['bonaj']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['bona'])

        raw_response = self.client.get(reverse('api_search_word', args=['bonajn']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['bona'])

    def test_search_precise_results_returns_canonical_table_word_form(self):
        word_obj = Word.objects.create(word="kiu")
        for variant in get_variants('kiu'):
            Variant.objects.create(word=word_obj, variant=variant)
        Morpheme.objects.create(primary_word=word_obj, morpheme="kiu")

        raw_response = self.client.get(reverse('api_search_word', args=['kiun']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['kiu'])

        raw_response = self.client.get(reverse('api_search_word', args=['kiuj']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['kiu'])

        raw_response = self.client.get(reverse('api_search_word', args=['kiujn']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['kiu'])

    def test_search_precise_results_returns_canonical_verb_form(self):
        word_obj = Word.objects.create(word="iri")
        for variant in get_variants('iri'):
            Variant.objects.create(word=word_obj, variant=variant)

        raw_response = self.client.get(reverse('api_search_word', args=['iras']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['iri'])

        raw_response = self.client.get(reverse('api_search_word', args=['iris']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['iri'])

        raw_response = self.client.get(reverse('api_search_word', args=['iros']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['iri'])

        raw_response = self.client.get(reverse('api_search_word', args=['irus']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['iri'])

        raw_response = self.client.get(reverse('api_search_word', args=['iru']))
        response = json.loads(raw_response.content)
        self.assertEqual(response['preciza'], ['iri'])

    def test_search_imprecise_results(self):
        word = Word.objects.create(word="hundo")
        Variant.objects.create(word=word, variant="hundo")

        raw_response = self.client.get(reverse('api_search_word', args=['zundo']))
        response = json.loads(raw_response.content)

        self.assertEqual(response['malpreciza'], ['hundo'])

    def test_search_imprecise_results_sorted(self):
        for word in ['sati', 'savi', 'bati', u'ŝati']:
            word_obj = Word.objects.create(word=word)
            for variant in get_variants(word):
                Variant.objects.create(word=word_obj, variant=variant)

        raw_response = self.client.get(reverse('api_search_word', args=['sati']))
        response = json.loads(raw_response.content)

        # We don't expect 'sati' in this list, as that will be in the precise search.
        self.assertEqual(response['malpreciza'], ['bati', 'savi', u'ŝati'])

    def test_search_word_building(self):
        word_obj = Word.objects.create(word="per")
        Morpheme.objects.create(primary_word=word_obj, morpheme="per")

        word_obj = Word.objects.create(word="soni")
        Morpheme.objects.create(primary_word=word_obj, morpheme="soni")
        Morpheme.objects.create(primary_word=word_obj, morpheme="son")

        word_obj = Word.objects.create(word="persono")
        Morpheme.objects.create(primary_word=word_obj, morpheme="persono")
        Morpheme.objects.create(primary_word=word_obj, morpheme="person")

        raw_response = self.client.get(reverse('api_search_word', args=['persone']))
        response = json.loads(raw_response.content)

        self.assertEqual(response['vortfarado'], [
            {'rezulto': 'person-e', 'partoj': ['persono']},
            {'rezulto': 'per-son-e', 'partoj': ['per', 'soni']},
        ])

    def test_search_translations(self):
        word_obj = Word.objects.create(word="hundo")
        definition = PrimaryDefinition.objects.create(
            word=word_obj, definition="besto")
        Translation.objects.create(word=word_obj, definition=definition,
                                   translation="dog", language_code="en")

        raw_response = self.client.get(reverse('api_search_word', args=['dog']))
        response = json.loads(raw_response.content)

        self.assertEqual(response['tradukoj'], [
            {'vorto': 'hundo', 'traduko': 'dog', 'kodo': 'en', 'lingvo': 'La angla'},
        ])
