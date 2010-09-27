from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from projektoj.vortaro.models import Word, Variant
from spelling import get_spelling_variations
from morphology import parse_morphology

def index(request):
    return render_to_response('vortaro/index.html', {},
                              context_instance=RequestContext(request))

def search_word(request):
    word = request.POST['vorto']
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

    # get morphological parsing results
    # of form [['konk', 'lud'], ['konklud']]
    potential_parsed_roots = parse_morphology(word)
    # convert to ['konk-lud', 'konklud']
    potential_parses = ['-'.join(roots) for roots in potential_parsed_roots]

    context = Context({'search_term':word,
                       'matching_words':matching_words,
                       'similar_words':similar_words,
                       'potential_parses':potential_parses})
    return render_to_response('vortaro/search.html', context,
                              context_instance=RequestContext(request))

def view_word(request, word):
    template = loader.get_template('vortaro/word.html')
    context = Context({'word':word})
    return HttpResponse(template.render(context))
