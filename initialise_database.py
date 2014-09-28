# -*- coding: utf-8 -*-
import json

from django.db import transaction

from vortaro.morphology import (
    is_declinable_adjective, is_declinable_noun, is_declinable_adverb,
    is_infinitive, is_pronoun,
)
from vortaro.models import (
    Word, Morpheme, Variant, PrimaryDefinition, Subdefinition, Translation,
    Example, Remark)

"""A simple script that populates the sqlite database from a JSON dump produced
by ReVo-utilities. Database must be empty to start with.

"""

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
    """Given a word, return a list of every possible legitimate
    spelling of it, in every tense, declension and writing system.

    We generate all our variants in lower case. Since we search over
    the variants, this gives us a case insensive search.

    """
    # the word itself is a variant
    word = word.lower()
    variants = [word]

    # every tense and declension
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
    elif is_pronoun(word):
        variants.extend([word + 'n'])

    # add additional variants if they are different in other writing
    # systems
    different = []
    for word in variants:
        if word != to_x_system(word):
            different.append(to_x_system(word))
        if word != to_h_system(word):
            different.append(to_h_system(word))

    variants.extend(different)

    return variants

@transaction.commit_on_success
def populate_database(dictionary):
    """Given a dictionary file from a JSON dump created by
    ReVo-utilities, write its contents to the database.

    We only commit once because it would take hours if we commit every
    object separately.

    """

    # no duplicate morphemes
    seen_morphemes = {}

    for (word, entry) in dictionary.items():

        word_obj = Word(word=word)
        word_obj.save()

        # variants (case/declension/tense)
        for variant in get_variants(word):
            Variant(word=word_obj, variant=variant).save()

        # add every definition
        # note this means that the order of definition_id corresponds
        # to the order of the definitions from ReVo, which is important
        for definition_dict in entry['definitions']:
            definition = definition_dict['primary definition']
            definition_obj = PrimaryDefinition(definition=definition,
                                               word=word_obj)
            definition_obj.save()

            # subdefinitions belonging to this definition
            for subdefinition_dict in definition_dict['subdefinitions']:
                subdefinition = subdefinition_dict['primary definition']
                subdefinition_obj = Subdefinition(definition=subdefinition,
                                                  root_definition=definition_obj)
                subdefinition_obj.save()

                # now all examples associated with this subdefinition
                for (example, source) in subdefinition_dict['examples']:
                    Example(definition=subdefinition_obj,
                            example=example, source=source).save()

                # all translations associated with this subdefinition
                for (language_code, translations) in subdefinition_dict['translations'].items():
                    for translation in translations:
                        Translation(word=word_obj, definition=subdefinition_obj,
                                    translation=translation,
                                    language_code=language_code).save()

            # examples belonging to this definition
            for (example, source) in definition_dict['examples']:
                Example(definition=definition_obj, example=example, 
                        source=source).save()

            # remarks belonging to this definition
            for remark in definition_dict['remarks']:
                Remark(definition=definition_obj, remark=remark).save()

            # words in other languages which have the same meaning
            for (language_code, translations) in definition_dict['translations'].items():
                for translation in translations:
                    Translation(word=word_obj, definition=definition_obj,
                                translation=translation,
                                language_code=language_code).save()

        # add morphemes to initial data
        if entry['primary']:
            """Primary means we will link to this word when we find
            the morpheme. For example, we link 'dorm' to 'dormi'
            although 'dormo' is also in the dictionary. 
            
            """
            # add morphemes (e.g. 'dorm'), forbidding those of one
            # letter since none actually exist in word buidling
            root = entry['root']
            if len(root) > 1 and root not in seen_morphemes:
                seen_morphemes[root] = True
                Morpheme(primary_word=word_obj, morpheme=root).save()

                # also add in other writing systems if different
                if to_h_system(root) not in seen_morphemes:
                    seen_morphemes[to_h_system(root)] = True
                    Morpheme(primary_word=word_obj,
                             morpheme=to_h_system(root)).save()

                if to_x_system(root) not in seen_morphemes:
                    seen_morphemes[to_x_system(root)] = True
                    Morpheme(primary_word=word_obj,
                             morpheme=to_x_system(root)).save()

        # also add words as morphemes if they end -o or -a
        if (is_declinable_noun(word) or is_declinable_adjective(word)) \
                and word not in seen_morphemes:
            seen_morphemes[word] = True
            Morpheme(primary_word=word_obj, morpheme=word).save()

            # and again also add if different in other writing systems
            if to_h_system(word) not in seen_morphemes:
                seen_morphemes[to_h_system(word)] = True
                Morpheme(primary_word=word_obj,
                         morpheme=to_h_system(word)).save()

            if to_x_system(word) not in seen_morphemes:
                seen_morphemes[to_x_system(word)] = True
                Morpheme(primary_word=word_obj,
                         morpheme=to_x_system(word)).save()

    # add -ant, etc morphemes which aren't in ReVo
    assert 'ant' not in seen_morphemes
    for morpheme in ['int', 'ant', 'ont', 'unt']:
        Morpheme(morpheme=morpheme).save()

    assert 'at' not in seen_morphemes
    for morpheme in ['it', 'at', 'ot']:
        Morpheme(morpheme=morpheme).save()

if __name__ == '__main__':
    dictionary_file = open('dictionary.json', 'r')
    dictionary = json.load(dictionary_file)
    populate_database(dictionary)
