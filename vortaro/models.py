# -*- coding: utf-8 -*-
from django.db import models

class Word(models.Model):
    """A term from the dictionary. Nouns will always be singular,
    verbs will always be infinitives and so on.

    """
    word = models.CharField(max_length=50, unique=True)
    definition = models.TextField()

    def __unicode__(self):
        return self.word

class Variant(models.Model):
    """A way of writing a term from the dictionary. Nouns may have
    plural or case endings, verbs can be in any tense and so on. We
    also allow the word to be in Unicode, h-system or
    x-system. Finally, a variant is always lower case -- this gives
    a case-insensitive search of the dictionary.

    We run the spellchecker against the list of variants as the
    user may have entered the word in any tense, capitalisation or
    writing system.

    An example:
    
    The variants of the word "aĉeti" will have include "aĉeti",
    "aĉetas", "aĉetu", "aĉetanta", "acxetis", "achetata" and so on.

    """

    word = models.ForeignKey(Word)
    variant = models.CharField(max_length=50)

    def __unicode__(self):
        return "{} (from {})".format(self.variant, self.word.word)
    
class Morpheme(models.Model):
    """A potential component of a word that has been put together. For
    example, in the word 'plifortigi' the morphemes would be 'pli',
    'fort' and 'ig'. 

    Since we may be splitting a word that has been written in any
    writing system, we generate potential morphemes in three writing
    systems: Unicode, x-system and h-system.

    Nouns may be used both with and without -o in word-building, so we
    allow both (dormosako / dormsako).

    Examples:

    "aĉeti" (verb) will have morphemes "aĉet", "acxet" and "achet"

    "per" (preposition) will have the morpheme "per"

    "dormo" (noun) will have morphemes "dorm" and "dormo"

    """

    primary_word = models.ForeignKey(Word)
    morpheme = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.morpheme
