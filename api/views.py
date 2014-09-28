import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from vortaro.models import Word
from vortaro.esperanto_sort import compare_esperanto_strings


# TODO: move to Django 1.7, which already provides this.
class JsonResponse(HttpResponse):
    def __init__(self, response_data, **kwargs):
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(json.dumps(response_data), **kwargs)


def view_word(request, word):
    word_obj = get_object_or_404(Word, word=word)

    definition_objs = word_obj.primarydefinition_set.all()

    definitions = [definition_obj.as_json() for definition_obj in definition_objs]

    return JsonResponse({
        'vorto': word_obj.word,
        'difinoj': definitions})


def search_word(request, search_term):
    matching_words = Word.objects.find_by_variant(search_term)

    similar_words = set(Word.objects.find_by_variant_fuzzy(search_term))
    similar_words = similar_words - set(matching_words)
    
    return JsonResponse({
        'preciza': [word.word for word in matching_words],
        'malpreciza': sorted([word.word for word in similar_words],
                             cmp=compare_esperanto_strings),
    })
