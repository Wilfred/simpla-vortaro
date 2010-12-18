# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from models import Word, Variant, PrimaryDefinition, Subdefinition, Example, Remark, Translation
from spelling import get_spelling_variations, alphabet
from morphology import parse_morphology
from esperanto_sort import compare_esperanto_strings

from projektoj.logger import Logger

log = Logger()

def about(request):
    return render_to_response('about.html', {})

def index(request):
    # all requests are dispatched from here, to keep URLs simple

    if 'vorto' in request.GET:
        word = request.GET['vorto'].strip()

        log.log_view_word(word, request.META['REMOTE_ADDR'])
        return render_word_view(word)
    elif u'serĉo' in request.GET:
        search_term = request.GET[u'serĉo'].strip()

        log.log_search(search_term, request.META['REMOTE_ADDR'])

        # allow users to go directly to a word definition if we can find one,
        # changing case if necessary:
        if 'rekte' in request.GET:
            # sadly sqlite does not support case insensitivity on utf8 strings
            if len(Word.objects.filter(word=search_term)) > 0:
                return render_word_view(search_term)

            if len(Word.objects.filter(word=search_term.lower())) > 0:
                return render_word_view(search_term.lower())

            # (note capitalisation doesn't work for ĉŝĝĵĥŭ -- FIXME)
            if len(Word.objects.filter(word=search_term.capitalize())) > 0:
                return render_word_view(search_term.capitalize())

        return render_word_search(search_term)
    else:
        return render_to_response('index.html', {})

def precise_word_search(word):
    """Find every possible term this word could be. Our variant table
    holds every possible conjugation and declension, so we just query
    that and remove duplicates.

    We return results in alphabetical order. However, the only way to
    get more than one result is if we have the same string in
    different cases, so really this just means lower case first.

    """
    matching_variants = Variant.objects.filter(variant=word)

    # find corresponding words, stripping duplicates
    matching_words = []
    for variant in matching_variants:
        if not variant.word in matching_words:
            matching_words.append(variant.word)

    # sort alphabetically
    compare = lambda x, y: compare_esperanto_strings(x.word, y.word)
    matching_words.sort(cmp=compare)

    return matching_words

def imprecise_word_search(word):
    """We generate alternative strings and also look them up in the
    dictionary. For very long words (13 letters or more) we generate
    too many alternatives so we only test the first 999 to keep sqlite
    happy.

    Results are returned in alphabetical order.

    """
    spelling_variations = get_spelling_variations(word)

    # limit for sqlite
    if len(spelling_variations) > 999:
        spelling_variations = spelling_variations[:999]

    # find matches
    matching_variants = Variant.objects.filter(variant__in=spelling_variations)

    # find corresponding words, stripping duplicates
    similar_words = []
    for variant in matching_variants:
        if (not variant.word in similar_words):
            similar_words.append(variant.word)

    # sort spelling variants into alphabetical order
    compare = lambda x, y: compare_esperanto_strings(x.word, y.word)
    similar_words.sort(cmp=compare)

    return similar_words

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

    grouped_translations = [[translations[0]]]
    for translation in translations[1:]:
        if translation.language == grouped_translations[-1][-1].language:
            grouped_translations[-1].append(translation)
        else:
            grouped_translations.append([translation])

    return grouped_translations

def render_word_search(search_term):
    # substitute ' if used, since e.g. vort' == vorto
    if search_term.endswith("'"):
        word = search_term[:-1] + 'o'
    else:
        word = search_term

    # if word is stupidly long, truncate it
    if len(word) > 40:
        word = word[:40]

    # strip any hyphens used, since we can't guarantee where they
    # will/will not appear
    word = word.replace('-', '')

    # all variants were stored lower case, so in case the user does
    # all caps:
    word = word.lower()

    matching_words = precise_word_search(word)

    # imprecise search, excluding those already found in the precise search
    similar_words = [term for term in imprecise_word_search(word)
                     if term not in matching_words]

    # get morphological parsing results
    # of form [['konk', 'lud'], ['konklud']]
    potential_parses = parse_morphology(word)

    # potential parses are weighted by likelihood, only show top two
    # since the rest are probably nonsensical
    potential_parses = potential_parses[:2]

    # get matching translations
    translations = translation_search(word)

    context = Context({'search_term':search_term,
                       'matching_words':matching_words,
                       'similar_words':similar_words,
                       'potential_parses':potential_parses,
                       'translations':translations})
    return render_to_response('search.html', context)

def render_word_view(word):
    # get the word
    matching_words = Word.objects.filter(word=word)

    # search instead if this word doesn't exist
    if len(matching_words) == 0:
        return HttpResponseRedirect(u'/?serĉo=' + word)

    # get definitions
    word_obj = matching_words[0]
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

    # we also pass an array of the esperanto alphabet for numbering
    context = Context({'word':word, 'definitions':definition_trees,
                       'translations': translations})
    return render_to_response('word.html', context)
