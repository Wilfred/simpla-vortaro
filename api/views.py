import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from vortaro.models import Word, Morpheme, Translation
from vortaro.esperanto_sort import compare_esperanto_strings
from vortaro.morphology import canonicalise_word, parse_morphology


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
    search_term = canonicalise_word(search_term)
    matching_words = Word.objects.find_by_variant(search_term)

    similar_words = set(Word.objects.find_by_variant_fuzzy(search_term))
    similar_words = similar_words - set(matching_words)

    parsed_words = []
    for parse_result in parse_morphology(search_term):
        printable_parts = []
        for part in parse_result:
            if isinstance(part, Morpheme):
                printable_parts.append(part.morpheme)
            else:
                printable_parts.append(part)

        parts = []
        for part in parse_result:
            if isinstance(part, Morpheme):
                parts.append({'vorto': part.primary_word.word,
                              'parto': part.morpheme})
            else:
                parts.append({'vorto': None, 'parto': part})
            
        parsed_words.append({
            'rezulto': "-".join(printable_parts),
            'partoj': parts,
        })

    translations = [
        {'vorto': trans.word.word, 'traduko': trans.translation,
         'kodo': trans.language_code, 'lingvo': trans.language}
        for trans in Translation.objects.filter(translation=search_term)
    ]
    
    return JsonResponse({
        'preciza': [word.word for word in matching_words],
        'malpreciza': sorted([word.word for word in similar_words],
                             cmp=compare_esperanto_strings),
        'vortfarado': parsed_words,
        'tradukoj': translations,
    })
