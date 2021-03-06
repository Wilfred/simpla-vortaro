# -*- coding: utf-8 -*-
from django.db import models

from spelling import get_spelling_variations


class WordManager(models.Manager):
    def find_by_variant(self, text):
        """Find every possible term this word could be. Our variant table
        holds every possible conjugation and declension.

        E.g. 'hundoj' -> we return the word 'hundo'.

        """
        # This can return multiple words in principle, in practice it
        # only seems to occur when we have two words that only differ by case.
        return Word.objects.filter(variant__variant=text)

    def find_by_variant_fuzzy(self, text):
        """Find every possible term that this word could be, tolerating
        spelling errors.

        E.g. 'hundjo' -> we return the word 'hundo' and 'hundejo'.

        """
        spelling_variations = get_spelling_variations(text)

        # SQLite can't handle more than 999 strings in an IN
        # query. This occurs for words of more than 12 characters.
        if len(spelling_variations) > 999:
            spelling_variations = spelling_variations[:999]

        return Word.objects.filter(variant__variant__in=spelling_variations)


class Word(models.Model):
    """A term from the dictionary, in its canonical form.

    Nouns will always be singular, verbs will always be infinitives
    and so on. For example, 'saluti', 'hundo'.

    """
    objects = WordManager()

    word = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.word

class Definition(models.Model):
    """A definition can either belong to a word (a PrimaryDefinition)
    or to another definition (a Subdefinition). Examples can be
    associated with either type, so we create a parent class.

    """
    definition = models.TextField(null=True)

    def __unicode__(self):
        return self.definition[:20]

    def as_json(self):
        return {
            'difino': self.definition,
            'ekzemploj': [example.as_json() for example in self.example_set.all()],
        }


class PrimaryDefinition(Definition):
    """A definition for a word. One word can have many primary
    definitions. The definition text may be null in a few rare
    circumstances where we only have subdefinitions. We shouldn't have
    any "" definitions.

    """
    word = models.ForeignKey(Word)

    def as_json(self):
        definition = super(PrimaryDefinition, self).as_json()
        definition['pludifinoj'] = [subdefinition.as_json()
                                    for subdefinition in self.subdefinition_set.all()]
        definition['tradukoj'] = [translation.as_json()
                                  for translation in self.translation_set.all()]

        return definition

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
    source = models.TextField(null=True)

    def __unicode__(self):
        return self.example[:20]

    def as_json(self):
        return {
            'ekzemplo': self.example,
            'fonto': self.source,
        }


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

    Since -ant, -int, -ont and -unt aren't in ReVo, we add them
    manually with a null primary_word. No other Morphemes should be
    like this.

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

    primary_word = models.ForeignKey(Word, null=True)
    morpheme = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        if self.primary_word:
            return u"%s (from %s)" % (self.morpheme, self.primary_word.word)
        else:
            return u"%s (no primary word)" % (self.morpheme,)


class Translation(models.Model):
    """The matching word for this definition of this word in another
    language.

    """
    # word is just a convenience to save us working out which word a
    # definition belongs to.
    word = models.ForeignKey(Word)
    definition = models.ForeignKey(Definition)
    translation = models.TextField()
    language_code = models.CharField(max_length=10)

    def as_json(self):
        return {
            'lingvo': self.language,
            'kodo': self.language_code,
            'traduko': self.translation,
        }

    @property
    def language(self):
        language_map = {
            'ab': u'La abĥaza', 'af': u'La afrikansa',
            'am': u'La amhara', 'ar': u'La araba',
            'as': u'La asama', 'ay': u'La ajmara',
            'az': u'La azerbajĝana', 'ba': u'La baŝkira',
            'be': u'La belorusa', 'bg': u'La bulgara',
            'bh': u'La bihara', 'bi': u'La bislama',
            'bn': u'La bengala', 'bo': u'La tibeta',
            'br': u'La bretona', 'ca': u'La kataluna',
            'co': u'La korsika', 'cs': u'La ĉeĥa',
            'cy': u'La kimra', 'da': u'La dana',
            'de': u'La germana', 'dz': u'La dzonka',
            'el': u'La greka', 'en': u'La angla',
            'eo': u'Esperanto', 'es': u'La hispana',
            'et': u'La estona', 'eu': u'La eŭska',
            'fa': u'La persa', 'fi': u'La finna',
            'fj': u'La fiĝia', 'fo': u'La feroa',
            'fr': u'La franca', 'fy': u'La okcidentfrisa',
            'ga': u'La irlanda', 'gd': u'La skotgaela',
            'gl': u'La galega', 'gn': u'La gvarania',
            'goyu': u'La tajvana', 'grc': u'La malnovgreka',
            'gu': u'La guĝarata', 'ha': u'La haŭsa',
            'he': u'La hebrea', 'hi': u'La hinda',
            'hr': u'La kroata', 'hu': u'La hungara',
            'hy': u'La armena', 'ia': u'Interlingvao',
            'id': u'La indonezia', 'ie': u'Okcidentalo',
            'ik': u'La inupiaka', 'io': u'Ido',
            'is': u'La islanda', 'it': u'La itala',
            'iu': u'La inuktituta', 'ja': u'La japana',
            'jbo': u'Loĵbano', 'jw': u'La java',
            'ka': u'La kartvela', 'kek': u'La kekĉia',
            'kk': u'La kazaĥa', 'kl': u'La gronlanda',
            'km': u'La kmera', 'kn': u'La kanara',
            'ko': u'La korea', 'ks': u'La kaŝmira',
            'ku': u'La kurda', 'ky': u'La kirgiza',
            'la': u'Latineca nomo', 'lat': u'Latino',
            'ln': u'La lingala', 'lo': u'La laŭa',
            'lt': u'La litova', 'lv': u'La latva',
            'mg': u'La malagasa', 'mi': u'La maoria',
            'mk': u'La makedona', 'ml': u'La malajalama',
            'mn': u'La mongola', 'mo': u'La moldava',
            'mr': u'La marata', 'ms': u'La malaja',
            'mt': u'La malta', 'my': u'La birma',
            'na': u'La naura', 'ne': u'La nepala',
            'nl': u'La nederlanda', 'no': u'La norvega',
            'oc': u'La okcitana', 'om': u'La oroma',
            'or': u'La odia', 'os': u'La oseta',
            'pa': u'La panĝaba', 'pl': u'La pola',
            'ps': u'La paŝtua', 'pt': u'La portugala',
            'qu': u'La keĉua', 'rm': u'La romanĉa',
            'rn': u'La burunda', 'ro': u'La rumana',
            'ru': u'La rusa', 'rw': u'La ruanda',
            'sa': u'Sanskrito', 'sd': u'La sinda',
            'se': u'La nordsamea', 'sg': u'La sangoa',
            'sh': u'La serbokroata', 'si': u'La sinhala',
            'sk': u'La slovaka', 'sl': u'La slovena',
            'sm': u'La samoa', 'sn': u'La ŝona',
            'so': u'La somala', 'sq': u'La albana',
            'sr': u'La serba', 'ss': u'La svazia',
            'st': u'La sota', 'su': u'La sunda',
            'sv': u'La sveda', 'sw': u'La svahila',
            'ta': u'La tamila', 'te': u'La telugua',
            'tg': u'La taĝika', 'th': u'La taja',
            'ti': u'La tigraja', 'tk': u'La turkmena',
            'tl': u'La filipina', 'tn': u'La cvana',
            'to': u'La tongaa', 'tp': u'Tokipono',
            'tr': u'La turka', 'ts': u'La conga',
            'tt': u'La tatara', 'tw': u'La akana',
            'ug': u'La ujgura', 'uk': u'La ukraina',
            'ur': u'Urduo', 'uz': u'La uzbeka',
            'vi': u'La vjetnama', 'vo': u'Volapuko',
            'wo': u'La volofa', 'xh': u'La kosa',
            'yi': u'La jida', 'yo': u'La joruba',
            'za': u'La ĝuanga', 'zh': u'La ĉina',
            'zu': u'La zulua'}

        return language_map[self.language_code]

    def __unicode__(self):
        return "%s: %s" % (self.language, self.translation)
