import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from vortaro.models import Word

# TODO: move to Django 1.7, which already provides this.
class JsonResponse(HttpResponse):
    def __init__(self, response_data, **kwargs):
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(json.dumps(response_data), **kwargs)


def view_word(request, word):
    word_obj = get_object_or_404(Word, word=word)

    definition_objs = word_obj.primarydefinition_set.all()
    definitions = [{'difino': definition_obj.definition}
                   for definition_obj in definition_objs]
    
    return JsonResponse({
        'vorto': word_obj.word,
        'difinoj': definitions})
