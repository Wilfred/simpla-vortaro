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

word_id = 0
def add_word(list_for_database, word):
    global word_id
    list_for_database.append({"pk": word_id, "model": "vortaro.word",
                             "fields": {'word': word}})
    word_id += 1

    # return id of the word we've just added so we can point to it
    return word_id - 1

variant_id = 0
def add_variant(list_for_database, variant, word_id):
    global variant_id
    list_for_database.append({"pk": variant_id, 
                              "model": "vortaro.variant",
                              "fields": {"variant": variant,
                                         "word": word_id}})
    variant_id += 1

definition_id = 0
def add_definition(list_for_database, definition_obj, word_id):
    """Given a definition object, create the correct definition,
    subdefinition and example rows for the database.

    """
    global definition_id

    # the definition table
    definition = definition_obj['primary definition']
    list_for_database.append({"pk": definition_id,
                              "model": "vortaro.definition",
                              "fields": {"definition": definition,
                                         "word": word_id}})

    # the subdefinitions (which will handle their own examples)
    subdefinitions = definition_obj['subdefinitions']
    for subdefinition in subdefinitions:
        add_subdefinition(list_for_database, subdefinition, definition_id)

    # examples belonging to this definition
    examples = definition_obj['examples']
    for example in examples:
        add_example(list_for_database, example, definition_id)

    definition_id += 1
    
subdefinition_id = 0
def add_subdefinition(list_for_database, subdefinition_obj,
                      definition_id):
    global subdefinition_id

    subdefinition = subdefinition_obj['primary definition']
    list_for_database.append({"pk":subdefinition_id,
                              "model":"vortaro.subdefinition",
                              "fields":{"root_definition":definition_id,
                                        "definition":subdefinition}})

    # now add all examples associated with this subdefinition
    examples = subdefinition_obj['examples']
    for example in examples:
        add_example(list_for_database, example, subdefinition_id)

    subdefinition_id += 1

morpheme_id = 0
def add_morpheme(list_for_database, root, word_id):
    global morpheme_id
    list_for_database.append({"pk": morpheme_id,
                              "model": "vortaro.morpheme",
                              "fields": {"primary_word": word_id,
                                         "morpheme": root}})
    morpheme_id += 1

example_id = 0
def add_example(list_for_database, example, definition_id):
    global example_id
    list_for_database.append({"pk": example_id,
                              "model": "vortaro.example",
                              "fields": {"definition": definition_id,
                                         "example": example}})
    example_id += 1

def dictionary_to_database(dictionary):
    """Given a list of dicts, prepare a list of initial data in a
    format that Django likes.

    """
    list_for_database = []

    added_morphemes = {}

    for (word, entry) in dictionary.items():
        # the word itself
        word_id = add_word(list_for_database, word)

        # variants (case/declension/tense)
        for variant in get_variants(word):
            add_variant(list_for_database, variant, word_id)

        # add every definition
        # note this means that the order of definition_id corresponds
        # to the order of the definitions from ReVo, which is important
        for definition in entry['definitions']:
            add_definition(list_for_database, definition, word_id)

        # add morphemes to initial data
        if entry['primary']:
            """Primary means we will link to this word when we find
            the morpheme. For example, we link 'dorm' to 'dormi'
            although 'dormo' is also in the dictionary. 
            
            """
            # add morphemes (e.g. 'dorm'), forbidding those of one
            # letter since none actually exist in word buidling
            root = entry['root']
            if len(root) > 1 and root not in added_morphemes:
                added_morphemes[root] = True
                add_morpheme(list_for_database, root, word_id)

                # also add in other writing system if different
                if to_h_system(root) not in added_morphemes:
                    added_morphemes[to_h_system(root)] = True
                    add_morpheme(list_for_database, to_h_system(root), word_id)

                if to_x_system(root) not in added_morphemes:
                    added_morphemes[to_x_system(root)] = True
                    add_morpheme(list_for_database, to_x_system(root), word_id)

        # also add words if they end -o or -a
        if (is_declinable_noun(word) or is_declinable_adjective(word)) \
                and word not in added_morphemes:
            added_morphemes[word] = True
            add_morpheme(list_for_database, word, word_id)

            # and again also add if different in other writing system
            if to_h_system(word) not in added_morphemes:
                added_morphemes[to_h_system(word)] = True
                add_morpheme(list_for_database, to_h_system(word), word_id)

            if to_x_system(word) not in added_morphemes:
                added_morphemes[to_x_system(word)] = True
                add_morpheme(list_for_database, to_x_system(word), word_id)

    return list_for_database

if __name__ == '__main__':
    dictionary_file = open('dictionary.json', 'r')
    dictionary = json.load(dictionary_file)

    initial_database = dictionary_to_database(dictionary)

    # todo: may need deletion
    # open and overwrite with the new initial data:
    output_file = open('initial_data.json', 'w')
    json.dump(initial_database, output_file)
