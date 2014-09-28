# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from models import Word, PrimaryDefinition, Subdefinition, Example, Remark, Translation
from .morphology import parse_morphology, canonicalise_word
from .esperanto_sort import compare_esperanto_strings


def about(request):
    return render(request, 'about.html')


def about_the_api(request):
    return render(request, 'about_the_api.html')


def index(request):
    # all requests are dispatched from here, to keep URLs simple

    if 'vorto' in request.GET:
        word = request.GET['vorto'].strip()
        return redirect('view_word', word)

    if u'serĉo' in request.GET:
        search_term = request.GET[u'serĉo'].strip()
        redirect_url = reverse('search_word')
        return redirect(redirect_url + u"?s=" + search_term)

    return render(request, 'index.html')


def view_word(request, word):
    # get the word
    try:
        word_obj = Word.objects.get(word=word)
    except Word.DoesNotExist:
        # Search instead if this word doesn't exist.
        redirect_url = reverse('search_word')
        return redirect(redirect_url + u"?s=" + word)

    # get definitions
    definitions = PrimaryDefinition.objects.filter(word=word_obj)

    # get any examples, remarks, subdefinitions and subdefinition examples
    definition_trees = []
    for definition in definitions:
        examples = Example.objects.filter(definition=definition)

        remarks = Remark.objects.filter(definition=definition)

        # get subdefinitions with index and examples
        # e.g. [('ĉ the definition', ['blah', 'blah blah']
        subdefinitions = Subdefinition.objects.filter(root_definition=definition)
        subdefs_with_examples = []
        for i in range(subdefinitions.count()):
            sub_examples = Example.objects.filter(definition=subdefinitions[i])
            subdefs_with_examples.append((subdefinitions[i].definition,
                                          sub_examples))

        # we want to count according the esperanto alphabet for subdefinitions
        definition_trees.append((definition, remarks, examples,
                                 subdefs_with_examples))

    # get translations for every definition and subdefinition
    translations = []
    for definition in definitions:
        definition_translations = list(Translation.objects.filter(definition=definition))
        definition_translations = group_translations(definition_translations)

        subdefinitions = Subdefinition.objects.filter(root_definition=definition)
        subdefinitions_translations = []
        for subdefinition in subdefinitions:
            subdefinition_translations = list(Translation.objects.filter(definition=subdefinition))
            subdefinition_translations = group_translations(subdefinition_translations)

            if subdefinition_translations:
                subdefinitions_translations.append(subdefinition_translations)

        if definition_translations or subdefinitions_translations:
            translations.append((definition_translations, subdefinitions_translations))

    return render(request, 'word.html',
                  {'word': word, 'definitions': definition_trees,
                   'translations': translations})


def search_word(request):
    query = request.GET[u's'].strip()
    search_term = canonicalise_word(query)

    # if search term is stupidly long, truncate it
    if len(search_term) > 40:
        search_term = search_term[:40]

    matching_words = Word.objects.find_by_variant(search_term)
    
    # allow users to go directly to a word definition if we can find one
    if 'rekte' in request.GET:
        if matching_words:
            return redirect('view_word', matching_words[0].word)

    # Fuzzy search, discarding words already found in the precise search.
    similar_words = set(Word.objects.find_by_variant_fuzzy(search_term))
    similar_words = similar_words - set(matching_words)

    # get morphological parsing results
    # of form [['konk', 'lud'], ['konklud']]
    potential_parses = parse_morphology(search_term)

    # get matching translations, ignoring changes we made for
    # esperanto words
    translations = translation_search(search_term)

    return render(request, 'search.html',
                  {'search_term':search_term,
                   'matching_words': matching_words,
                   'similar_words':similar_words,
                   'potential_parses':potential_parses,
                   'translations':translations})


def translation_search(search_term):
    translations = list(Translation.objects.filter(translation=search_term))

    return group_translations(translations)

def group_translations(translations):
    """Given a list of translations, group into a list of lists where each
    sublist only contains translations of one language. Assumes the list is
    already sorted by language.

    """
    if not translations:
        return []

    translations.sort(key=(lambda t: t.language), cmp=compare_esperanto_strings)

    grouped_translations = [[translations[0]]]
    for translation in translations[1:]:
        if translation.language == grouped_translations[-1][-1].language:
            grouped_translations[-1].append(translation)
        else:
            grouped_translations.append([translation])

    return grouped_translations
