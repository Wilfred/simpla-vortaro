#!/usr/bin/python
# -*- coding: utf-8 -*-

raw_alphabet = ['a', 'b', 'c', 'ĉ', 'd', 'e', 'f', 'g', 'ĝ', 'h', 'ĥ',
                'i', 'j', 'ĵ', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
                'ŝ', 't', 'u', 'ŭ', 'v', 'z']
alphabet = [letter.decode('utf8') for letter in raw_alphabet]
    
def transpose(word, position):
    # swap letter at position with letter at position+1
    letters = list(word)

    temp = letters[position]
    letters[position] = letters[position+1]
    letters[position+1] = temp

    return ''.join(letters)

def delete_letter(word, position):
    # remove letter at position in word
    letters = list(word)

    letters.pop(position)

    return ''.join(letters)

def insert_letter(word, position, letter):
    # insert letter at position in word
    letters = list(word)

    letters.insert(position, letter)

    return ''.join(letters)

def replace_letter(word, position, letter):
    # put letter at position at word, overwriting current
    letters = list(word)

    letters[position] = letter

    return ''.join(letters)

def get_spelling_variations(word):
    """Get every possible spelling variation of this string. We
    assume that only one mistake has been made.

    This code only considers lower case words. The resulting
    complexity is O(57n+29), where n is the number of characters in
    the string.

    Somewhat inspired by http://norvig.com/spell-correct.html

    """
    variations = []

    # transpositions
    # complexity O(n-1)
    for i in range(len(word)-1):
        variations.append(transpose(word, i))

    # deletions
    # complexity O(n)
    for i in range(len(word)):
        variations.append(delete_letter(word, i))

    # insertions
    # complexity O(28n+28)
    for letter in alphabet:
        for i in range(len(word)+1):
            variations.append(insert_letter(word, i, letter))

    # insertion of hyphen in the case of affixes
    # complexity O(2)
    variations.append(word + '-')
    variations.append('-' + word)

    # replacements, taking care not to recreate the original word
    # complexity O(27n)
    for i in range(len(word)):
        for letter in alphabet:
            if word[i] != letter:
                variations.append(replace_letter(word, i, letter))

    return variations
