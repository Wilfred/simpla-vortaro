from django.http import HttpResponse
from django.template import Context, loader

from projektoj.vortaro.models import Word, Variant
from spelling import get_spelling_variations

def index(request):
    template = loader.get_template('vortaro/index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def search_word(request, word):
    # find all words that match this search term, regardless of variant
    matching_variants = Variant.objects.filter(variant=word)
    matching_words = []
    for variant in matching_variants:
        if not variant.word in matching_words:
            matching_words.append(variant.word)

    # find all potential spelling variants  of this search term
    spelling_variations = get_spelling_variations(word)
    matching_variants = Variant.objects.filter(variant__in=spelling_variations)
    similar_words = []
    for variant in matching_variants:
        if (not variant.word in similar_words) and (not variant.word in matching_words):
            similar_words.append(variant.word)

    template = loader.get_template('vortaro/search.html')
    context = Context({'search_term':word,
                       'matching_words':matching_words,
                       'similar_words':similar_words})
    return HttpResponse(template.render(context))

def view_word(request, word):
    template = loader.get_template('vortaro/word.html')
    context = Context({'word':word})
    return HttpResponse(template.render(context))
