# -*- coding: utf-8 -*-

from models import Morpheme

"""A few methods for establishing what kind of word a given word
is. This is particularly useful for generating every possible form of
a word -- we want to product "bluaj" from "blua" but not "laj" from
"la" and so on.

"""

def is_infinitive(word):
    if not word.endswith(u'i'):
        return False
    
    pronouns = [u'mi', u'vi', u'li', u'ŝi', u'ĝi', u'oni', u'ili', u'si', u'ci']
    adverbs = [u'ĉi']
    exclamations = [u'ahi', u'fi']
    abbreviations = [u'ĥi'] # same as ĥio actually
    affix = [u'-ologi']
    preposition = [u'pli']

    if word in (pronouns + adverbs + exclamations + abbreviations +
                affix + preposition):
        return False
    
    return True

def is_declinable_adjective(word):
    table_words = [u'ĉiu', u'tiu', u'neniu', u'iu', u'kiu']
    if word in table_words:
        return True

    if not word.endswith(u'a'):
        return False

    onomatopoeia = [u'ta'] # to be precise, it's "ta ta ta"
    exclamations = [u'hura', u'pa', u'aha', u'ba', u'ha']
    prepositions = [u'tra', u'la', u'ja']

    if word in (onomatopoeia + exclamations + prepositions):
        return False

    return True

def is_declinable_noun(word):
    if not word.endswith(u'o'):
        return False

    exclamation = [u'ho']
    # we list the prefices for completeness
    # although they arguably end u'-'
    affices = [u'-o', u'bo-', u'geo-']
    conjunction = [u'do']
    preposition = [u'po']

    if word in (exclamation + affices + conjunction + preposition):
        return False

    return True

def is_declinable_adverb(word):
    # Be warned: I'm not sure that every adverb makes sense
    # with -n

    if not word.endswith(u'e'):
        return False

    preposition = [u'de', u'je', u'ĉe']
    exclamation = [u'he', u've', u'ehe']
    conjunction = [u'ke']
    particle = [u'ne'] # vague category I know, but nothing else fits
    fixed_adverbs = [u'tre']
    name = [u'Kabe']
    affix = [u'tele-']

    if word in (preposition + exclamation + conjunction + particle +
                fixed_adverbs + name + affix):
        return False

    return True

def parse_morphology(word):
    # stem, then split into roots
    # currently only does -o, -a, -e, -i for stemming

    if is_infinitive(word) or is_declinable_noun(word) or \
            is_declinable_adjective(word) or \
            is_declinable_adverb(word):
        stem, ending = word[:-1], word[-1]
        parses =  find_roots(stem)
        return [parse + [ending] for parse in parses]
    
    # doesn't appear to have an ending we can get rid of
    return find_roots(word)

def find_roots(compound):
    """Given a word that has been put together using Esperanto roots,
    find those roots. We do this by working left to right and building
    up a list of all possible radikoj according to the substrings seen
    so far.

    Since we assume roots are intact, the suffices -ĉjo and -njo which
    modify the roots cannot be used with this approach.

    For a given string, there are 2^(n-1) possible ways to split it
    into substrings so this algorithm is potentially
    exponential. However, since we work left to right and don't
    examine the remainder if a prefix isn't valid, the performance
    isn't much worse than linear.

    Examples worth thinking about: senvestigi, persone (is a pun and
    has two parses), birdkanto, birdokanto, sobrakape (seen in the
    wild), ĝustatempe, serĉante

    Examples:

    >>> find_roots(u'plifortigas')
    [[u'pli', u'fort', u'ig', u'as']]

    >>> find_roots(u'persone')
    [[u'person', u'e'], [u'per', u'son', u'e']]

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

    """In the event of multiple possible splits of this word, we
    consider the split made of the fewest morphemes to be valid. Given
    'konklud' as input, we assume that 'konklud-' is more likely than
    'konk-' 'lud-'. To this end we sort it so fewer splits come first.

    """
    splits.sort(reverse=True)

    return splits

def find_matching(word):
    # note we will need to consider both full words and roots
    # e.g. 'dormoĉambro' -> 'dormo' 'ĉambr' (after stemming)

    matches = Morpheme.objects.filter(morpheme=word)
    assert len(matches) < 2
    if len(matches) == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    print parse_morphology(u'konkludo')
