from django.http import HttpResponse
from django.template import Context, loader

from projektoj.vortaro.models import Word

def index(request):
    template = loader.get_template('vortaro/index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def search_word(request, word):
    matching_words = [w.word for w in Word.objects.filter(word=word)]

    template = loader.get_template('vortaro/word.html')
    context = Context({'search_term':word, 'matching_words':matching_words})
    return HttpResponse(template.render(context))
