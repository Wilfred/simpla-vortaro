# -*- coding: utf-8 -*-
import json
from vortaro.morphology import *
from copy import copy

def to_h_system(word):
    h_system = {u'ĉ':u'ch', u'Ĉ':u'Ch', u'ĝ':u'gh', u'Ĝ':u'Gh', u'ĥ':u'hh',
                u'Ĥ':u'Hh', u'ĵ':u'jh', u'Ĵ':u'Jh', u'ŝ':u'sh', u'Ŝ':u'Sh',
                u'ŭ':u'u', u'Ŭ':u'U'}
    output = []
    for letter in list(word):
        if letter in h_system.keys():
            output.append(h_system[letter])
        else:
            output.append(letter)
    return ''.join(output)

def to_x_system(word):
    x_system = {u'ĉ':u'cx', u'Ĉ':u'Cx', u'ĝ':u'gx', u'Ĝ':u'Gx', u'ĥ':u'hx',
                u'Ĥ':u'Hx', u'ĵ':u'jx', u'Ĵ':u'Jx', u'ŝ':u'sx', u'Ŝ':u'Sx',
                u'ŭ':u'ux', u'Ŭ':u'Ux'}
    output = []
    for letter in list(word):
        if letter in x_system.keys():
            output.append(x_system[letter])
        else:
            output.append(letter)
    return ''.join(output)

def get_variants(word):
    # every possible legitimate spelling of this word, always lower
    # case to give a case insensitive sort (see vortaro/models.py)
    variants = [word.lower()]

    if is_infinitive(word):
        root = word[:-1]
        variants.extend([root + 'is', root + 'as', root + 'os', 
                          root + 'us', root + 'u'])
    elif is_declinable_adjective(word):
        variants.extend([word + 'j', word + 'n', word + 'jn'])
    elif is_declinable_noun(word):
        variants.extend([word + 'j', word + 'n', word + 'jn'])
    elif is_declinable_adverb(word):
        variants.extend([word + 'n'])

    for word in copy(variants):
        if word != to_x_system(word):
            variants.append(to_x_system(word))
        if word != to_h_system(word):
            variants.append(to_h_system(word))

    return variants

if __name__ == '__main__':
    """Open the dictionary dump, generate all the possible variants
    in a format that Django likes.

    """
    dictionary = open('dictionary.json', 'r')

    initial_data = []

    variant_id = 0
    morpheme_id = 0
    added_morphemes = []
    for (word_id, entry) in enumerate(json.load(dictionary)):
        # the word itself
        word = entry['word']
        definition = entry['definition']
        initial_data.append({"pk":word_id, "model":"vortaro.word",
                             "fields":{'word':word,
                                       'definition':definition}})

        # variants (case/declension/tense)
        for variant in get_variants(entry["word"]):
            initial_data.append({"pk":variant_id, 
                                 "model":"vortaro.variant",
                                 "fields":{"variant":variant,
                                           "word":word_id}})
            variant_id += 1

        """Add morphemes to initial data. We forbid single letter
        morphemes (none actually exist in word-building) but permit -o
        and -a endings of words in addition to the root (e.g. we add
        both 'dom' and 'domo').

        Note that the following words produce clashes: sumo, halo,
        nova, togo, vila, koto, metro, polo, alo. This is because we
        cannot distinguish between (for example) metro and metroo in
        the context of word-building.

        """

        if entry['primary']:
            """Primary means we will link to this word when we find
            the morpheme. For example, we link 'dorm' to 'dormi'
            although 'dormo' is also in the dictionary. 
            
            """

            # add word roots (e.g. 'dorm')
            root = entry['root']
            if len(root) > 1 and root not in added_morphemes:
                initial_data.append({"pk":morpheme_id,
                                     "model":"vortaro.morpheme",
                                     "fields":{"primary_word":word_id,
                                               "morpheme":root}})
                added_morphemes.append(root)
                morpheme_id += 1

            # add words if they end -o or -a
            if (is_declinable_noun(word) or is_declinable_adjective(word)) \
                    and word not in added_morphemes:
                initial_data.append({"pk":morpheme_id,
                                     "model":"vortaro.morpheme",
                                     "fields":{"primary_word":word_id,
                                               "morpheme":word}})
                added_morphemes.append(word)
                morpheme_id += 1
                

    # TODO: may need to delete the original file
    output_file = open('initial_data.json', 'w')
    json.dump(initial_data, output_file)
