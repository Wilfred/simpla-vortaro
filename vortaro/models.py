# -*- coding: utf-8 -*-
from django.db import models

class Word(models.Model):
    """A term from the dictionary. Nouns will always be singular,
    verbs will always be infinitives and so on.

    """
    word = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.word

class Definition(models.Model):
    """A definition can either belong to a word (a PrimaryDefinition)
    or to another definition (a Subdefinition). Examples can be
    associated with either type, so we create a parent class.

    """
    definition = models.TextField(null=True)

class PrimaryDefinition(Definition):
    """A definition for a word. One word can have many primary
    definitions. The definition text may be null in a few rare
    circumstances where we only have subdefinitions. We shouldn't have
    any "" definitions.

    """
    word = models.ForeignKey(Word)

class Subdefinition(Definition):
    """A subdefinition of a specfic definition. One definition can
    have none or many subdefinitions. As with Definition, we allow
    null.

    """
    root_definition = models.ForeignKey(PrimaryDefinition)

class Example(models.Model):
    """A string that holds a sentence which shows usage of a specific
    definition of a word. One definition can have many examples.

    """
    definition = models.ForeignKey(Definition)
    example = models.TextField()

class Remark(models.Model):
    """A string that holds a remark about a definition. One definition
    can have multiple remarks.

    """
    definition = models.ForeignKey(Definition)
    remark = models.TextField()

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
        return self.variant
    
class Morpheme(models.Model):
    """A potential component of a word that has been put together. We
    generate morphemes in all three major writing systems, and also
    allow words ending -o or -a to be used wholesale.

    Note that the following words produce clashes: 
    
    sumo, haplo, nova, togo, vila, koto, metro, polo, alo --
    because they could be <word> or <word>o

    Sauda Arabujo/Saŭda Arabujo and Sauda-Arabujo/Saŭda-Arabujo --
    because in the h-system we don't know which of the pair to pick.

    For example, in the word 'plifortigi' the morphemes would be
    'pli', 'fort' and 'ig'.

    Examples:

    "aĉeti" (verb) will have morphemes "aĉet", "acxet" and "achet"

    "per" (preposition) will have the morpheme "per"

    "dormo" (noun) will have morphemes "dorm" and "dormo"

    """

    primary_word = models.ForeignKey(Word)
    morpheme = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.morpheme
