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
