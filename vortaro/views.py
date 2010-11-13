# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from models import Word, Variant, Definition, Subdefinition, Example
from spelling import get_spelling_variations, alphabet
from morphology import parse_morphology
from esperanto_sort import compare_esperanto_strings

def about(request):
    return render_to_response('about.html', {})

def index(request):
    # all requests are dispatched from here, to keep URLs simple

    if u'vorto' in request.GET:
        return view_word(request.GET[u'vorto'])
    elif u'serĉo' in request.GET:
        return search_word(request.GET[u'serĉo'])
    else:
        return render_to_response('index.html', {})

def search_word(search_term):
    # substitute ' if used, since e.g. vort' == vorto
    if search_term.endswith("'"):
        word = search_term[:-1] + 'o'
    else:
        word = search_term

    # strip any hyphens used, since we can't guarantee where they
    # will/will not appear
    word = word.replace('-', '')

    # find all words that match this search term, regardless of
    # variant and avoiding duplicates
    matching_variants = Variant.objects.filter(variant=word)
    matching_words = []
    for variant in matching_variants:
        if not variant.word in matching_words:
            matching_words.append(variant.word)

    # return matches in alphabetical order
    # (in practice this means lower case first since the words are
    # exact matches)
    compare = lambda word_x, word_y: compare_esperanto_strings(word_x.word,
                                                               word_y.word)
    matching_words.sort(cmp=compare)

    # test as many possible spellings of this search term as possible
    # within the 999 variable limit of sqlite
    spelling_variations = get_spelling_variations(word)
    if len(spelling_variations) > 999:
        spelling_variations = spelling_variations[:999]

    matching_variants = Variant.objects.filter(variant__in=spelling_variations)
    similar_words = []
    for variant in matching_variants:
        if (not variant.word in similar_words) and (not variant.word in matching_words):
            similar_words.append(variant.word)

    # sort spelling variants into alphabetical order
    similar_words.sort(cmp=compare)

    # get morphological parsing results
    # of form [['konk', 'lud'], ['konklud']]
    potential_parses = parse_morphology(word)

    context = Context({'search_term':search_term,
                       'matching_words':matching_words,
                       'similar_words':similar_words,
                       'potential_parses':potential_parses})
    return render_to_response('search.html', context)

def view_word(word):
    # get the word
    matching_words = Word.objects.filter(word=word)

    # search instead if this word doesn't exist
    if len(matching_words) == 0:
        return HttpResponseRedirect(u'/?serĉo=' + word)

    # get definitions
    word_obj = matching_words[0]
    definitions = Definition.objects.filter(word=word_obj)

    # get any examples, subdefinitions and subdefinition examples
    definition_trees = []
    for definition in definitions:
        examples = Example.objects.filter(definition=definition)

        # get subdefinitions with index and examples
        # e.g. [('ĉ', 'the definition', ['blah', 'blah blah']
        subdefinitions = Subdefinition.objects.filter(root_definition=definition)
        numbered_subdefs_with_examples = []
        for i in range(subdefinitions.count()):
            sub_examples = Example.objects.filter(definition=subdefinitions[i])
            numbered_subdefs_with_examples.append((alphabet[i],
                                                  subdefinitions[i].definition,
                                                  sub_examples))

        # we want to count according the esperanto alphabet for subdefinitions
        definition_trees.append((definition, examples, numbered_subdefs_with_examples))

    # we also pass an array of the esperanto alphabet for numbering
    context = Context({'word':word, 'definitions':definition_trees,
                       "alphabet": alphabet})
    return render_to_response('word.html', context)
