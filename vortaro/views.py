from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    template = loader.get_template('vortaro/index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def search_word(request, word):
    return HttpResponse(word + " was searched.")
