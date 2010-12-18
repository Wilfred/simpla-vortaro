# -*- coding: utf-8 -*-
# this file is part of ReVo-utilities and development happens there

def compare_esperanto_strings(x_mixed_case, y_mixed_case):
    # alphabetical sort of esperanto strings
    # (not unicode strings, normal strings)
    # permitting whole latin alphabet (so including q, x etc)
    # falling back on unicode ordering for unknown characters

    # need utf8 strings or we cannot iterate over them
    # esperanto uses multibyte characters
    
    if type(x_mixed_case) == str:
        x = x_mixed_case.decode('utf8').strip()
    else:
        x = x_mixed_case.strip()
    if type(y_mixed_case) == str:
        y = y_mixed_case.decode('utf8').strip()
    else:
        y = y_mixed_case.strip()

    # we explicitly add ' ' and '-' to the alphabet
    # ' ' is first in the alphabet so 'a b' comes before 'ab'
    # '-' is second so that affixes come first

    alphabet = [u' ', u'-', u'a', u'A', u'b', u'B', u'c', u'C', u'ĉ', u'Ĉ',
                u'd', u'D', u'e', u'E', u'f', u'F', u'g', u'G', u'ĝ', u'Ĝ',
                u'h', u'H', u'ĥ', u'Ĥ', u'i', u'I', u'j', u'J', u'ĵ', u'Ĵ',
                u'k', u'K', u'l', u'L', u'm', u'M', u'n', u'N', u'o', u'O',
                u'p', u'P', u'q', u'Q', u'r', u'R', u's', u'S', u'ŝ', u'Ŝ',
                u't', u'T', u'u', u'U', u'ŭ', u'Ŭ', u'v', u'V', u'w', u'W',
                u'x', u'X', u'y', u'Y', u'z', u'Z']
    
    for i in range(min(len(x),len(y))):
        try:
            if alphabet.index(x[i]) < alphabet.index(y[i]):
                return -1
            elif alphabet.index(x[i]) > alphabet.index(y[i]):
                return 1
        except ValueError:
            # not in alphabet
            if x[i] in alphabet:
                return -1
            elif y[i] in alphabet:
                return 1
            else:
                # neither character in alphabet, use normal unicode ordering
                if x < y:
                    return -1
                elif x > y:
                    return 1

    # if one string is the prefix of the other we reach this point

    # longer strings come afterwards
    if len(x) < len(y):
        return -1
    elif len(x) > len(y):
        return 1
    else:
        # completely identical
        return 0
