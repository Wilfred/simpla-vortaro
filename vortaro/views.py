from django.http import HttpResponse
from django.template import Context, loader

from projektoj.vortaro.models import Word
from spelling import get_variations

def index(request):
    template = loader.get_template('vortaro/index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def search_word(request, word):
    precise_matches = [w.word for w in Word.objects.filter(word=word)]
    
    variations = get_variations(word)
    imprecise_matches = []
    for variation in variations:
        imprecise_matches += [w.word for w in Word.objects.filter(word=variation)]

    template = loader.get_template('vortaro/search.html')
    context = Context({'search_term':word,
                       'precise_matches':precise_matches,
                       'imprecise_matches':imprecise_matches})
    return HttpResponse(template.render(context))

def view_word(request, word):
    return HttpResponse("Vi vidas " + word)
