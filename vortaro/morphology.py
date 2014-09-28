# -*- coding: utf-8 -*-

from models import Morpheme

"""Esperanto morphology tools. We have methods for identifying word
type, for stemming and for parsing combined words.

A major use of this code is for generating every possible form of a
word -- we want to produce "bluaj" from "blua" but not "laj" from "la"
and so on.

For the split_* methods, these have been cross checked using the
following commands to find exceptions (singular nouns in this
example):

fish> egrep -iw '^.*o$' <word_list.txt | awk '{ print length(), $0 | "sort -n" }' | less

"""

def split_verb(word):
    """If this word is a verb, return a tuple of the stem and the
    ending. Otherwise, return None.

    We consider every tense, but ignore participles (-anta, -ata etc).

    """
    # infinitives
    if word.endswith('i'):
        # *i words that are not verbs:
        pronouns = [u'mi', u'vi', u'li', u'ŝi', u'ĝi', u'oni', u'ili', u'si', u'ci']
        adverbs = [u'ĉi']
        exclamations = [u'ahi', u'fi']
        abbreviations = [u'ĥi'] # same as ĥio actually
        affix = [u'-ologi']
        preposition = [u'pli']

        if word in (pronouns + adverbs + exclamations + abbreviations +
                    affix + preposition):
            return None
        else:
            return (word[:-1], 'i')

    if word.endswith('is'):
        exclamation = ['bis']
        prefix = ['mis']
        preposition = [u'ĝis']
        names = [u'Ĝenĝis', u'Ĝinĝis']

        if word in (exclamation + prefix + preposition + names):
            return None
        else:
            return (word[:-2], 'is')

    if word.endswith('as'):
        # no exceptions as far as I'm aware
        return (word[:-2], 'as')

    if word.endswith('os'):
        # also no exceptions it seems
        return (word[:-2], 'os')

    if word.endswith('us'):
        adverb = [u'ĵus']
        conjunctions = ['plus', 'minus']
        if word in (adverb + conjunctions):
            return None
        else:
            return (word[:-2], 'us')

    if word.endswith('u'):
        table_words = ['kiu', u'ĉiu', 'tiu', 'neniu', 'iu']
        numbers = ['unu', 'du']
        onomatopoeia = ['fu']
        interjections = ['hu', 'nu']
        adverbs = ['ju', 'plu']
        conjunction = [u'ĉu']
        if word in (table_words + numbers + onomatopoeia +
                    interjections + adverbs + conjunction):
            return None
        else:
            return (word[:-1], 'u')

    return None

def split_adjective(word):
    """If the word is an adjective, return a tuple of the stem and the
    ending. Otherwise return None.

    """
    if word.endswith('a'):
        onomatopoeia = ['ta'] # to be precise, it's "ta ta ta"
        exclamations = ['hura', 'pa', 'aha', 'ba', 'ha']
        prepositions = ['tra', 'la', 'ja']
        if word in (onomatopoeia + exclamations + prepositions):
            return None
        else:
            return (word[:-1], 'a')

    if word.endswith('aj'):
        exclamation = ['aj']
        conjunction = ['kaj']
        if word in (exclamation + conjunction):
            return None
        else:
            return (word[:-2], 'aj')

    if word.endswith('an'):
        names = ['Osman', 'Jordan']
        if word in names:
            return None
        else:
            return (word[:-2], 'an')

    if word.endswith('ajn'):
        if word == 'ajn':
            return None
        else:
            return (word[:-3], 'ajn')

    # table words ending -u act as adjectives
    if word.endswith('u'):
        table_words = ['kiu', u'ĉiu', 'tiu', 'neniu', 'iu']
        if word in table_words:
            return (word[:-1], 'u')
        else:
            return None

    if word.endswith('uj'):
        # arguably 'neniuj' doesn't exist, but for the sake of completeness
        table_words = ['kiuj', u'ĉiuj', 'tiuj', 'neniuj', 'iuj']
        if word in table_words:
            return (word[:-2], 'uj')
        else:
            return None

    if word.endswith('un'):
        table_words = ['kiun', u'ĉiun', 'tiun', 'neniun', 'iun']
        if word in table_words:
            return (word[:-2], 'un')
        else:
            return None

    if word.endswith('ujn'):
        # also arguably 'neniujn' doesn't exist
        table_words = ['kiujn', u'ĉiujn', 'tiujn', 'neniujn', 'iujn']
        if word in table_words:
            return (word[:-3], 'ujn')
        else:
            return None

    return None

def split_noun(word):
    """Split a word into a tuple of its stem and its ending, if it's a
    noun. Otherwise return None.

    """
    if word.endswith('o'):
        exclamation = ['ho']
        # we list the prefices for completeness
        # although they arguably end '-'
        affices = ['-o', 'bo-', 'geo-']
        conjunction = ['do']
        preposition = ['po']
        if word in [exclamation + affices + conjunction + preposition]:
            return None
        else:
            return (word[:-1], 'o')

    if word.endswith('oj'):
        if word == 'oj': # exclamation
            return None
        else:
            return (word[:-2], 'oj')

    if word.endswith('on'):
        if word == 'Simeon': # name
            return None
        else:
            return (word[:-2], 'on')

    if word.endswith('ojn'):
        # appears there are no exceptions
        return (word[:-3], 'ojn')

    return None

def split_adverb(word):
    """Split a word into a tuple of its stem and its ending, if it's
    an adjective. Otherwise return None.

    I'm not convinced every adverb actually makes sense with an -en
    ending, but we deal with all the exceptions I've found.

    """
    if word.endswith('e'):
        preposition = ['de', 'je', u'ĉe']
        exclamation = ['he', 've', 'ehe']
        conjunctions = ['ke', 'se']
        particle = ['ne'] # vague category I know, but nothing else fits
        fixed_adverbs = ['tre']
        name = ['Kabe']
        affix = ['tele-'] # again affices only for completeness
        if word in (preposition + exclamation + conjunctions + 
                    particle + fixed_adverbs + name + affix):
            return None
        else:
            return (word[:-1], 'e')

    if word.endswith('en'):
        prepositions = ['en', 'sen']
        adverb = ['jen']
        affix = ['sen-']
        name = ['Eden']
        exclamation = ['amen']
        if word in (prepositions + adverb + affix + name + exclamation):
            return None
        else:
            return (word[:-2], 'en')

    return None

def is_pronoun(word):
    if word in ['mi', 'vi', 'li', u'ŝi', 'ni', 'ili', 'si', 'ci']:
        return True

    return False

def is_infinitive(word):
    if split_verb(word):
        (stem, ending) = split_verb(word)
        if ending == 'i':
            return True

    return False

def is_declinable_adjective(word):
    if split_adjective(word):
        (stem, ending) = split_adjective(word)
        if ending == 'a' or ending == 'u' or ending == 'i':
            return True

    return False

def is_declinable_noun(word):
    if split_noun(word):
        (stem, ending) = split_noun(word)
        if ending == 'o':
            return True

    return False

def is_declinable_adverb(word):
    # Be warned: I'm not sure that every adverb makes sense
    # with -n
    if split_adverb(word):
        (stem, ending) = split_adverb(word)
        if ending == 'e':
            return True

    return False

def score_parse(parse):
    """Given a parse (a list of Morphemes plus optional string
    ending), return a badness score so we can sort for
    likelihood. Values for this function have been tuned using
    test_parser.py.

    """
    # ignore string endings from stemmer
    if type(parse[-1]) == str:
        parse = parse[:-1]

    # fewer, longer morphemes is more likely
    badness = len(parse)

    # well known affixes are more likely
    # (which ones specifically to include chosen by trial and error)
    for affix in ['ig', 'il', 'ul', 'ej', 'in', 'an', 'ar', 'ant',
                  'int', 'ont', 'at', 'it', 'ot', 'al', 'em']:
        for morpheme in parse:
            if morpheme.morpheme == affix:
                badness -= 0.5

    return badness

def parse_morphology(word):
    # potential parses are weighted by likelihood, only show top two
    # since the rest are probably nonsensical
    return parse_morphology_all(word)[:2]


def parse_morphology_all(word):
    """Given a word (possibly constructed using word-building
    ('vortfarado'), stem it (if possible) then split it into its
    constituent roots.

    We return a list of Morpheme objects followed (optionally) by a
    string of the ending.

    """
    assert isinstance(word, basestring)

    # for table words, just get them as-is
    if word in [u'ĉio', 'cxio', 'chio', 'nenio', 'tio', 'io', 'kio',
                u'ĉiu', 'cxiu', 'chiu', 'neniu', 'tiu', 'iu', 'kiu',
                u'ĉie', 'cxie', 'chie', 'nenie', 'tie', 'ie', 'kie',
                u'ĉia', 'cxia', 'chia', 'nenia', 'tia', 'ia', 'kia']:
        return [[find_matching(word)]]

    # for table words with -j or -n endings, print 'nenio-n' instead of 'neni-on'
    if word in [u'ĉion', 'cxion', 'chion', 'nenion', 'tion', 'ion', 'kion',
                u'ĉiun', 'cxiun', 'chiun', 'neniun', 'tiun', 'iun', 'kiun',
                u'ĉien', 'cxien', 'chien', 'nenien', 'tien', 'ien', 'kien',
                u'ĉian', 'cxian', 'chian', 'nenian', 'tian', 'ian', 'kian']:
        return [[find_matching(word[:-1]), 'n']]

    if split_verb(word):
        (stem, ending) = split_verb(word)
        parses = find_roots(stem)
        return [parse + [ending] for parse in parses]

    if split_adjective(word):
        (stem, ending) = split_adjective(word)
        parses = find_roots(stem)
        return [parse + [ending] for parse in parses]

    if split_noun(word):
        (stem, ending) = split_noun(word)
        parses = find_roots(stem)
        return [parse + [ending] for parse in parses]

    if split_adverb(word):
        (stem, ending) = split_adverb(word)
        parses = find_roots(stem)
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

    >>> find_roots('plifortigas')
    [['pli', 'fort', 'ig', 'as']]

    >>> find_roots('persone')
    [['person', 'e'], ['per', 'son', 'e']]

    """

    if compound == "":
        return [[]]

    splits = []
    for i in range(1, len(compound) + 1):
        match = find_matching(compound[0:i])
        if not match is None:
            # this seems to be a valid word or root
            # so see if the remainder is valid
            endings = find_roots(compound[i:])
            # todo: ending is not an ideal variable name
            for ending in endings:
                splits.append([match] + ending)

    # if there are multiple parses, try to make the first one the most
    # likely possibility
    splits.sort(key=score_parse)

    return splits

def find_matching(word):
    """See if this word is a valid morpheme in the database. If so,
    return it."""
    # note we will need to consider both full words and roots
    # e.g. 'dormoĉambro' -> 'dormo' 'ĉambr' (after stemming)

    matches = Morpheme.objects.filter(morpheme=word)
    assert len(matches) < 2
    if len(matches) == 1:
        return matches[0]
    else:
        return None


def canonicalise_word(word):
    """Given a word, convert it to a canonical form that matches how we
    store words in our database.

    >>> canonicalise_word("Mal-salut' ") # a silly word
    "malsaluto"

    """
    word = word.strip()
    
    # substitute ' if used, since e.g. vort' == vorto
    if word.endswith("'"):
        word = word[:-1] + 'o'

    # Strip any hyphens used, since we can't guarantee where they
    # will/will not appear.
    clean_word = word.replace('-', '')
    # However, we have words in the dictionary that start with hyphens,
    # e.g. '-eg', so we want to preserve hyphens in that case.
    if word.startswith('-'):
        clean_word = '-' + clean_word

    # Our variants are stored in lower case, so ensure we match.
    clean_word = clean_word.lower()

    return clean_word


if __name__ == '__main__':
    print parse_morphology(u'konkludo')
