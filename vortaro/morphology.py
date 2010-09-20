#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A few methods for establishing what kind of word a given word
is. This is particularly useful for generating every possible form of
a word -- we want to product "bluaj" from "blua" but not "laj" from
"la" and so on.

"""

def is_infinitive(word):
    if not word.endswith('i'):
        return False
    
    pronouns = ['mi', 'vi', 'li', 'ŝi', 'ĝi', 'oni', 'ili', 'si', 'ci']
    adverbs = ['ĉi']
    exclamations = ['ahi', 'fi']
    abbreviations = ['ĥi'] # same as ĥio actually
    affix = ['-ologi']
    preposition = ['pli']

    if word in (pronouns + adverbs + exclamations + abbreviations +
                affix + preposition):
        return False
    
    return True

def is_declinable_adjective(word):
    table_words = ['ĉiu', 'tiu', 'neniu', 'iu', 'kiu']
    if word in table_words:
        return True

    if not word.endswith('a'):
        return False

    onomatopoeia = ['ta'] # to be precise, it's "ta ta ta"
    exclamations = ['hura', 'pa', 'aha', 'ba', 'ha']
    prepositions = ['tra', 'la', 'ja']

    if word in (onomatopoeia + exclamations + prepositions):
        return False

    return True

def is_declinable_noun(word):
    if not word.endswith('o'):
        return False

    exclamation = ['ho']
    # we list the prefices for completeness
    # although they arguably end '-'
    affices = ['-o', 'bo-', 'geo-']
    conjunction = ['do']
    preposition = ['po']

    if word in (exclamation + affices + conjunction + preposition):
        return False

    return True

def is_undeclinable_adverb(word):
    # Be warned: I'm not sure that every adverb makes sense
    # with -n

    if not word.endswith('e'):
        return False

    preposition = ['de', 'je', 'ĉe']
    exclamation = ['he', 've', 'ehe']
    conjunction = ['ke']
    particle = ['ne'] # vague category I know, but nothing else fits
    fixed_adverbs = ['tre']
    name = ['Kabe']
    affix = ['tele-']

    if word in (preposition + exclamation + conjunction + particle +
                fixed_adverbs + name + affix):
        return False

    return True

def find_word_roots(word):
    # stem, then split into roots

    # todo: need to stem properly
    compound = word[:-1]
    return find_roots(compound)

def find_roots(compound):
    """Given a word that has been put together using Esperanto roots,
    find those roots. We do this by working left to right and building
    up a list of all possible radikoj according to the substrings seen
    so far.

    In the worse case this is O(2^n) where n is the number of
    characters in the input string, but in practice the number of
    entries in the dictionary means that it won't be much worse than
    linear.

    Examples:

    >>> find_roots('plifortigas')
    [['pli', 'fort', 'ig']]

    >>> find_roots('persone')
    [['person'], ['per', 'son']]

    """

    if compound == "":
        return [[]]

    splits = []
    for i in range(1, len(compound) + 1):
        if find_matching(compound[0:i]):
            # this seems to be a valid word or root
            # so see if the remainder is valid
            endings = find_roots(compound[i:])
            # todo: ending is not an ideal variable name
            for ending in endings:
                splits.append([compound[0:i]] + ending)
    return splits

def find_matching(word):
    # mockup until DB contains proper roots
    # note we need to consider both full words and roots
    # e.g. 'dormoĉambro' -> 'dormo' 'ĉambr' (after stemming)

    words = ['pli', 'sen', 'forta', 'vesti', 'persona', 'sono', 'per',
             'igi', 'iĝi', 'konkludo', 'dormo', 'ĉambro', 'konko', 'ludo']
    # avoiding duplicates
    roots = ['fort', 'vest', 'person', 'son', 'ig', 'iĝ', 'konklud',
             'dorm', 'ĉambr', 'konk', 'lud']

    return word in (words + roots)

if __name__ == '__main__':
    print find_word_roots('konkludo')
